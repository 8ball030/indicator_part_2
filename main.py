#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Tom Rae
Authorised use only
"""
import pandas as pd
import tensortrade.env.default as default

from tensortrade.data.cdd import CryptoDataDownload
from tensortrade.feed.core import Stream, DataFeed
from tensortrade.oms.exchanges import Exchange
from tensortrade.oms.services.execution.simulated import execute_order
from tensortrade.oms.instruments import USD, BTC, ETH
from tensortrade.oms.wallets import Wallet, Portfolio
from tensortrade.agents import DQNAgent


from ta import add_all_ta_features
from ta.utils import _ema


import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def load_data(base="USD", counter="BTC", period="1h", last_n=2000):
    """Read in the raw data for the market."""
    logger.info(f"Loading price data for {base}/{counter}")
    cdd = CryptoDataDownload()
    data = cdd.fetch("Bitstamp", base, counter, period)
    data = add_all_ta_features(data, 
                               "open", 
                               "high", 
                               "low",
                               "close",
                               "volume")
    data = data[['date', 'unix', 'low', 'close', 'open', 'volume', 'high', 'volume_vwap', 'volume_nvi', 'volume_adi',
       'volatility_bbm', 'trend_sma_fast', 'volume_fi', 'trend_adx_pos',
       'volatility_bbw']]
    data = data.iloc[-last_n:]
    return data


def setup_environment(data, feed):
    """Create environment."""
    logger.info(f"Creating environment.")
    coinbase = Exchange("coinbase", service=execute_order)(Stream.source(
        list(data["close"]), dtype="float").rename("USD-BTC"))

    portfolio = Portfolio(
        USD, [Wallet(coinbase, 10000 * USD),
              Wallet(coinbase, 0 * BTC)])

    renderer_feed = DataFeed([
        Stream.source(list(data["date"])).rename("date"),
        Stream.source(list(data["open"]), dtype="float").rename("open"),
        Stream.source(list(data["high"]), dtype="float").rename("high"),
        Stream.source(list(data["low"]), dtype="float").rename("low"),
        Stream.source(list(data["close"]), dtype="float").rename("close"),
        Stream.source(list(data["volume"]), dtype="float").rename("volume")
    ])

    env = default.create(portfolio=portfolio,
                         action_scheme="simple",
                         reward_scheme="simple",
                         feed=feed,
                         renderer_feed=renderer_feed,
                         renderer=default.renderers.FileLogger(),
                         window_size=20)
    return env


def train_agent(env):
    """Training agent."""
    logger.info(f"Training Agent.")




    agent = DQNAgent(env)

    agent.train(n_steps=2000, n_episodes=10000, save_path="agents/")




def create_feed(data: pd.DataFrame):
    """Create feed to be used by Tensor Trader."""
    logger.info(f"Creating feed")

    def rsi(price: Stream[float], period: float) -> Stream[float]:
        """Apply rsi calc."""
        r = price.diff()
        upside = r.clamp_min(0).abs()
        downside = r.clamp_max(0).abs()
        rs = upside.ewm(alpha=1 / period).mean() / downside.ewm(alpha=1 /
                                                                period).mean()
        return 100 * (1 - (1 + rs)**-1)

    def macd(price: Stream[float], fast: float, slow: float,
             signal: float) -> Stream[float]:
        """apply macd calcuation."""
        fm = price.ewm(span=fast, adjust=False).mean()
        sm = price.ewm(span=slow, adjust=False).mean()
        md = fm - sm
        signal = md - md.ewm(span=signal, adjust=False).mean()
        return signal

    # here we add out custom indicators
    # todo
    def volatility_bbm(price: Stream[float], 
                       window: int = 20,
                       window_dev: int = 2
                       ):
        win = price.rolling(window=window, min_periods=window)
        return win.mean()
        
    def volatility_bbw(price: Stream[float], 
                       window: int = 20,
                       window_dev: int = 2):
        mavg = price.rolling(window=window, min_periods=window).mean()
        mstd =price.rolling(window=window, min_periods=window).std()
        hband = mavg + window_dev * mstd
        lband = mavg - window_dev * mstd
        wband = ((hband - lband)/mavg) * 100
        return wband

    def volume_vwap(high: Stream[float],
                    low: Stream[float],
                    close: Stream[float],
                    volume: Stream[float],
                    window: int=14,
                    ):
        price = (high + low + close) / 3
        
        typical_price_volume = price * volume
        
        total_pv = typical_price_volume.rolling(window=window, min_periods=window).sum()
        total_vol = volume.rolling(window=window, min_periods=window).sum()
        
        vwap = total_pv / total_vol

        return vwap

    def volume_adi(high: Stream[float],
                   low: Stream[float],
                   close: Stream[float],
                   volume: Stream[float],
                   ):
        clv = ((close - low) - (high - close)) / (high - low)
        adi = clv * volume
        return adi.cumsum()

    def volume_fi(close: Stream[float],
                  volume: Stream[float],
                  window: int = 13
                  ):
        import pdb; pdb.set_trace()

        fi = (close - close.shift(1)) * volume
        fi = _ema(window)
        return fi

    def volume_nvi(close: Stream[float],
                   volume: Stream[float],):
        price_change = close.pct_change()
        vol_decrease = volume.shift(1) > volume
        nvi = pd.Series(
            data=np.nan, index=close.index, dtype="float64", name="nvi"
        )
        nvi.iloc[0] = 1000
        for i in range(1, len(nvi)):
            if vol_decrease.iloc[i]:
                nvi.iloc[i] = nvi.iloc[i - 1] * (1.0 + price_change.iloc[i])
            else:
                nvi.iloc[i] = nvi.iloc[i - 1]
        return nvi
        
    def trend_adx_pos(price: Stream[float]):
        raise NotImplementedError

    def trend_sma_fast(price: Stream[float]):
        raise NotImplementedError
    

        

    features = []
    for c in data.columns[1:]:
        s = Stream.source(list(data[c]), dtype="float").rename(data[c].name)
        features += [s]

    # cp = Stream.select(features, lambda s: s.name == "close")
    # lp = Stream.select(features, lambda s: s.name == "low")
    # hp = Stream.select(features, lambda s: s.name == "high")
    # v = Stream.select(features, lambda s: s.name == "volume")

    # features = [
    #     cp.log().diff().rename("lr"),
    #     rsi(cp, period=20).rename("rsi"),
    #     macd(cp, fast=10, slow=50, signal=5).rename("macd"),
    #     volatility_bbm(cp),
    #     volatility_bbw(cp),
    #     volume_vwap(hp, lp, cp, v),
    #     volume_adi(hp, lp, cp, v),
    #     volume_fi(cp, v),
    #     
    # ]

    feed = DataFeed(features)
    feed.compile()
    return feed


def main():
    data = load_data()
    feed = create_feed(data)
    env = setup_environment(data, feed)
    train_agent(env)


if __name__ == "__main__":
    main()

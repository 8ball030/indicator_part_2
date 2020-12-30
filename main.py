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
    return transform_data(data, last_n)

def transform_data(data, last_n):
    data = add_all_ta_features(data, 
                               "open", 
                               "high", 
                               "low",
                               "close",
                               "volume")
    data = data[['date', 'unix', 'low', 'close', 'open', 'volume', 'high', 
                 'volume_vwap', 'volume_nvi', 'volume_adi', 'volatility_bbm', 
                 'trend_sma_fast', 'volume_fi', 'trend_adx_pos', 'volatility_bbw']]
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

    agent.train(n_steps=2000, 
                n_episodes=10000,
                save_path="agents/")


def create_feed(data: pd.DataFrame):
    """Create feed to be used by Tensor Trader."""
    logger.info(f"Creating feed")
    features = []
    for c in data.columns[1:]:
        s = Stream.source(list(data[c]), dtype="float").rename(data[c].name)
        features += [s]

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

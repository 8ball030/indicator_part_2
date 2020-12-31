# FTX Indicator Series

## Part II

### Introduction


### Study on biased coin flip and Decision making


### Study on 

## Paper

Technical Indicators  - Part 2

Introduction
Our previous article on the selection of technical indicators saw an investigation into the information conveyed in a large number of traditional financial technical indicators. We performed an analysis of the markets involved in FTX’s trading DeFi trading competition to determine the indicators which convey the most information at each timestep.

By employing a machine learning algorithm to predict the next time step in the series, we were able to use the technical indicators as factors in this prediction problem. We were then able to isolate the impact of each of the individual indicators in order to rank their impact on the models ability to correctly predict the next time step.

We were able to show that for the vast majority of the technical indicators, their inclusion into our model did not increase our predictive capability. It also allowed us to identify the most relevant indicators as so;


The next issue becomes, how do we capitalise on this knowledge? A more traditional approach to the problem would be to create a rule-based system. Using a rule based system, the architect would specify individual combinations of if condition then actions that will feel intuitive. These rule-based systems would then be backtested against historic market data in order to optimise the performance of the system.

However, this approach has a number of drawbacks. 
Requires an approach to assigning buy and sell signals to the different combinations of possible factors.
Can require a large number of rules to cover every outcome
The solution space is huge.

It is clear that more traditional forms of computing will not necessarily help us achieve our desired outcome of outperforming the market, the solution space is too large, and the difficulty in implementing enough rules to cover every possible case is impractical.

Traditional Machine Learning
In traditional Machine Learning, the main approaches are Supervised Learning, where we have labeled data to use for training. This is the approach that is most known and seen in the real world. Common applications of this approach are for classification. In recent years there has been a huge shift forward in the technology used to actually perform this classification beginning with the success of (FIND REFERNECE) in the image net challenges hosted by Google in 2008/2009.
This approach used a neural network based on the human brain to classify images that allowed it to exceed human level performance in a number of common image classification tasks, and in the passing decade, the technology has improved considerably. 

Unsupervised Machine Learning is the other traditional branch of Machine Learning, it is primarily concerned with finding association vast datasets. The intuition behind Unsupervised Machine Learning is that the architect is able to present the algorithm the data and the algorithm will identify patterns in the data that would be impossible to discern using traditional methods. The technology is most commonly known to be used in recommendation systems, i.e. the product recommendation engine used by Amazon is an example of this type of Machine Learning.

We could apply either of these traditional approaches to the time-series data that we have collected for the market. For example, we could use Supervised Machine Learning along with our pre-selected indicators to go ahead and predict the direction of the market over the next time step. Alternatively, we could go ahead and use Unsupervised Learning to categorise periods of the market into different categories based on relationships between the technical indicators we would be unable to identify without considerable computational cost.

However, it is clear that even if we were to provide a signal to our trading decisions, we would still be missing a vital component required to fully automate the system. Speak to any experienced trader, one of the most important things about success in the trading area is behaviour, not just picking the right moves, but knowing what to do when it goes wrong. Discipline, and sticking to your system is vital to survival as a trader.

To fully capitalise on the information gained from the indicators we have selected, it would still be necessary to create a number of rules to manage exposure, position size, and existing orders. All of these interacting rules opens up the possibility of unintended consequences, or would require considerable testing to cover every conceivable situation.

Therefore, we are looking for a different approach to exploring the solution space. Due to the fact that our actions within the environment have a direct impact upon our performance within the environment, the problem does not fit into the traditional domains for which machine learning is best known for. 





Reinforcement Learning
Reinforcement Learning is a more modern approach to decision making in incomplete non-deterministic environments. The technique sprung to fame emerged into the forefront of decision making computer science with the performance of the AI  Go playing algorithm developed by Deep Mind. This algorithm comprehensively annihilated the world's best human Go player in XXXX. 
This achievement was revolutionary for the field, and in the passing time, the technology has been applied with startling results in a number of fields from playing Super Mario on Nintendo, through to performing stunts in remote controlled planes. What makes this form of learning so interesting is that the algorithms are able to map actions from many time steps in the past to rewards achieved in the present time step. Additionally the algorithm is capable of reacting to new information and updating its model to account for the new information.

The core concept underlying Reinforcement Learning is that the algorithms are designed to perform actions on a modelled environment constructed to match the real world as much as possible. The algorithm will then take an action on that environment and then depending upon the action, the agent will then either receive a reward or not receive a reward. 

At each step, the agent will predict which action will deliver the most expected long term reward, the results of the action are then used by the agent to update its expected reward with the reward actually received. Continued iterations of this process lead to the agent learning which actions will maximise its expected long term reward.


This form of Machine Learning has already been applied to trading by a number of different authors with very promising results, XXXXXXX 





Experiment
Continuing with our datasets gathered from the previous article, we will use the TensorTrader library to implement our trading agent. Selected indicators on our data to create a vector consisting of a number of features;
The technical Indicators applied to the OHLCV bars.
The internal state of the Agent. Cash balance / Asset Balance.
. We will then implement a Reinforcement Learning algorithm which as its reward measure receives the simple profit and loss of the agent through its current iteration. This metric means that our algorithm will optimise the actions of the agent in order to maximise profit, with no regard for risk. There are a number of different performance measures we would use in order to change the behaviour of our agent, depending upon our personal risk tolerance, these will be covered in the next article as we discuss the real world performance of our agent.




Results

Conclusion



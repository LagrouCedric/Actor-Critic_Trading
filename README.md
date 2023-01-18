# Research Project 
### Cedric Lagrou

## Installation Guideline
#### ToDo

# Environment
#### based on: https://medium.com/coinmonks/deep-reinforcement-learning-for-trading-cryptocurrencies-5b5502b1ece1
## Features
### full Feature list:
#### 'open', 'High', 'Low', 'CLose', 'Invested money', 'non-invested', 'invested_amount of crypto', 'Unix Time', 'MACD', 'SMA60K', 'SMA30K', 'LastBuy', 'LastSold', 'LastBuyPrice', 'LastSoldPrice' 

### Why these features?
#### I used the OHLC as features, because that's what represents the price of the currency at a certain time. The model can use this to help predict a good action for this timestamp.

#### We also have some calculated features, this article helped me with some of them
#### https://academy.swissborg.com/en/learn/crypto-trading-indicators
#### From this article i used:
#### -- Simple Moving Average (SMA)
#### -- Moving Average Convergence Divergence (MACD)
####
#### MACD Formula: MACD=12-Period EMA − 26-Period EMA
#### These are calculated in the environment and put into the dataframe for quicker use during the training
####
#### Last of we also give the information when the model last bought and sold and the prices of those, so he can focus on getting good results

## Researching Reward System
#### The reward is split into 3 parts ( the actions ): 'Hold', 'Buy' and 'Sell'

### HOLD: 
#### in the holding part, we check if the chosen action == 0 ( hold), and we always give a negative reward of 25 to reduce overfiting to action 0 ( that happened when reward was '0')

### Buy:
#### First we check if the current invested money is more than 75% of our current worth e.g. worth = 20.000 --> max invested = 15.000
#### Secondly we check if one of our latest actions was a buy or sell, because we want the AI to know not to sell immediatly or buy everything at once without thinking it's a good buy 
#### If in one of the steps the action doesn't meet the requirement, we return a negative reward, otherwise we Buy and return a postive reward

### Sell:
#### We first check if we have money invested if not, negative reward
#### then we go on to check if we didn't buy or sell in the latest actions, otherwise negative reward
#### if it meets the requirements, the invested amount of Crypto will get fictionally sold, giving a postive reward if it earns more money then invested, and a negative one if it loses money


# Agent

## Agent choice
#### To choose a good reinforcement learning agent, i started with a simple implementation of a DQN agent and an actor critic.
#### The actor critic quickly learned a couple things, whilst the DQN was doing overfitting on one action or randomly picking things, it didn't learn well / quick enough to use this as an agent for this project.
#### for the remainder of this project I will not focus on the DQN implementation, because the training time will make it harder to create and actor critic is an overal better option to use in this case

#### The actor critic performed well, so i went on with the development of that certain agent

## agent explained
#### the actor critic is split into 3 networks: 'Policy', 'Actor' and 'Critic'
#### simply said, the policy choses an action by having an actor picking an action he thinks is best and a critic network evaluating that certain action the actor picked

## saving the agent
#### I can easily save the 3 models in a folder by using the keras save ( & load) build in functions

## training the model
#### the model itself get trained on the environment with a maxIterations and a number of episodes at a time, we also save some data to make some visals in the end to show the progress of our model and to see where it bought and sold
#### The training is then evaluated in a shorter 'Demo' testset, to see if how it scores, the testset is chosen so it has the opportunity to make some good profits and to check where it bought and sold.
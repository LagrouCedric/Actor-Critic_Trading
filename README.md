# Research Project 
### Cedric Lagrou

## Installation Guideline
#### ToDo

# Environment
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
#### MACD Formula
#### MACD=12-Period EMA − 26-Period EMA
#### These are calculated in the environment and put into the dataframe

## Researching Reward System
##
### The reward is split into 3 parts: 'Hold', 'Buy' and 'Sell'

### HOLD: 
#### in the holding part, we check if the chosen action == 0 ( hold), and we always give a negative reward of 25 to reduce overfiting to action 0 ( that happened when reward was '0')

### Buy:
#### First we check if the current invested money is more than 15.000, 75% of our initial investment
#### Secondly we check if one of our latest actions was a buy or sell, because we want the AI to know not to sell immediatly
#### If in one of the steps the action doesn't meet the requirement, we return a negative reward, otherwise we Buy and return a postive reward

### Sell:
#### We first check if we have money invested if not, negative reward
#### then we go on to check if we didn't buy or sell in the latest actions, otherwise negative reward
#### if it meets the requirements, the invested amount of Crypto will get fictionally sold, giving a postive reward if it earns more money then invested, and a negative one if it loses money


# Agent
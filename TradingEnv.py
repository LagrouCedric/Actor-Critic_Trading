#First tradingEnv class
#todo add transaction cost
# add MACD indicator
# add RSI indicator
# add SMA indicator
# add EMA indicator
# meerdere crypto's toevoegen ( momenteel alleen BTC)
import numpy as np
import pandas as pd
class TradingEnv():
    def __init__(self, initial_investment=20000, Terminal_state= 2000):
        #investment
        self.initial_investment = initial_investment #initial investment 
        self.Terminal_state = Terminal_state  #terminal state, when the agent reach this state or below, the episode is over
        self.current_investment = initial_investment #current investment in a certain state
        self.non_invested = initial_investment #non invested money in a certain state
        self.invested = 0
        self.worth_history = [] #worth history in a certain episode
        # self.invested = [{'amount': 0, 'price_investment': 0, 'timestamp' : UNIX timestamp of investment}] #invested money 
        self.invested_amount = 0
        
        #rewards
        self.current_reward = 0 #current reward in a certain state
        self.total_reward = 0   #total reward in a certain episode
        self.reward_history = [] #reward history in a certain episode
        self.iterations = 0

        #states
        self.current_price = [0,0,0,0] #current price in a certain state [open,high,low,close]
        self.prev_price = np.zeros(20) #previous 20 prices to keep in memory to the state values
        self.done = False #if the episode is over
        self.current_unix_time = 0 #current unix time in a certain state
        self.macd = 0 #macd indicator
        
        
        #actions
        self.action = 0 #chosen action in a certain state
        self.action_history = [] #action history in a certain episode
        self.action_space = np.array([0,1,2]) #action space, 0 = hold, 1 = buy, 2 = sell first in the array 

        #Current state
        # self.current_state = self.get_current_state() #current state
        self.csv_to_dataframe() #convert csv's to one dataframe
        self.csv_index = 0 #index of the csv dataframe


    def get_current_state(self):
        #return current state price, and invested/non invested values as state
        return [self.current_price[0],self.current_price[1],self.current_price[2],self.current_price[3], self.invested, self.non_invested, self.invested_amount, self.current_unix_time]
    def calculate_macd(self):
        #calculate macd indicator
        macd = self.df.iloc[self.csv_index - 12 : self.csv_index, 3].ewm(span=12, adjust=False).mean()
        return macd
    def reset(self):
        #reset the environment
        self.worth_history = []
        self.current_investment = self.initial_investment
        self.current_reward = 0
        self.total_reward = 0
        self.reward_history = []
        self.current_price = [0,0,0,0] #current price in a certain state [open,high,low,close]
        self.invested_amount = 0
        self.non_invested = self.initial_investment #non invested money in a certain state
        self.invested = 0
        self.worth_history = [] #worth history in a certain episode

        self.prev_price = np.zeros(20)
        self.action = 0
        self.action_history = []
        self.done = False
        self.current_unix_time = 0 #current unix time in a certain state
        self.csv_index = 0 #index of the csv dataframe


        #begin somewhere random in csv data 
        
        self.csv_index = np.random.randint(0, (len(self.df)/2) + 500)
        #get row csv_index from self.df
        self.current_price = self.df.iloc[self.csv_index, 3:7].values
        self.current_unix_time = self.df.iloc[self.csv_index, 0]
        
        self.macd = self.calculate_macd()



        return self.get_current_state(), self.done

    def step(self, action):
        self.iterations += 1
        self.action = action
        self.action_history.append(self.action)

        #calculate current reward
        self.current_reward = self.get_reward()
        self.done = self.is_done()
        #if the episode is over, give a big negative reward
        if self.done == True:
            self.current.reward - 1000000

        self.total_reward += self.current_reward
        self.reward_history.append(self.current_reward)

        #get next line of data in csv
        if self.csv_index < len(self.df) - 1:
            self.csv_index += 1
            self.current_price = self.df.iloc[self.csv_index, 3:7].values
            self.current_unix_time = self.df.iloc[self.csv_index, 0]
        else:
            self.done = True
        return self.get_current_state(), self.current_reward, self.done
        
    def get_reward(self):
        #reward function
        if self.action == 0:
            #hold do nothing
            reward = 0
        elif self.action == 1:
            #buy = invest 1/10 of non_invested money
            to_invest = self.non_invested / 10
            self.non_invested -= to_invest
            amount = to_invest / self.current_price[0]
            self.invested += to_invest
            self.invested_amount += amount
            reward = 0
        elif self.action == 2:
            #sell first bought in array of invested
            if self.invested > 0:
                amount = self.invested_amount
                price_investment = self.invested
                self.non_invested += amount * self.current_price[0]
                self.invested_amount = 0
                self.invested = 0

                reward = (amount * self.current_price[0]) - price_investment
            else:
                #hold, do nothing, nothing to sell
                reward = 0
        
        self.worth_history.append(self.calc_current_worth())
        return reward


    def is_done(self):
        #terminal state
        if self.calc_current_worth() <= self.Terminal_state:
            return True
        else:
            return False

    def calc_current_worth(self):
        #calculate current worth
        return self.invested_amount * self.current_price[0] + self.non_invested

        
    def csv_to_dataframe(self):
        #convert csv's to one dataframe
        df2017 = pd.read_csv('./data/BTC-2017min.csv')
        df2018 = pd.read_csv('./data/BTC-2018min.csv')
        df2019 = pd.read_csv('./data/BTC-2019min.csv')
        df2020 = pd.read_csv('./data/BTC-2020min.csv')
        df2021 = pd.read_csv('./data/BTC-2021min.csv')

        #concat all dataframes
        df = pd.concat([df2017, df2018, df2019, df2020, df2021], ignore_index=True)
        self.df = df
        #len = 2675301
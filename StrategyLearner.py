""""""
"""  		  	   		   	 			  		 			 	 	 		 		 	
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		   	 			  		 			 	 	 		 		 	
Atlanta, Georgia 30332  		  	   		   	 			  		 			 	 	 		 		 	
All Rights Reserved  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
Template code for CS 4646/7646  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		   	 			  		 			 	 	 		 		 	
works, including solutions to the projects assigned in this course. Students  		  	   		   	 			  		 			 	 	 		 		 	
and other users of this template code are advised not to share it with others  		  	   		   	 			  		 			 	 	 		 		 	
or to make it available on publicly viewable websites including repositories  		  	   		   	 			  		 			 	 	 		 		 	
such as github and gitlab.  This copyright statement should not be removed  		  	   		   	 			  		 			 	 	 		 		 	
or edited.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
We do grant permission to share solutions privately with non-students such  		  	   		   	 			  		 			 	 	 		 		 	
as potential employers. However, sharing with other current or future  		  	   		   	 			  		 			 	 	 		 		 	
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		   	 			  		 			 	 	 		 		 	
GT honor code violation.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
-----do not edit anything above this line---  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
Student Name: Shahrzad Amoozegar   		  	   		   	 			  		 			 	 	 		 		 	
GT User ID: samoozegar3  		  	   		   	 			  		 			 	 	 		 		 	
GT ID: 903650161    		  	   		   	 			  		 			 	 	 		 		 	
"""

import datetime as dt

import pandas as pd
import util as ut
import RTLearner as rt
import BagLearner as bl
import indicators as ind

import numpy as np
import matplotlib.pyplot as plt

class StrategyLearner(object):
    """  		  	   		   	 			  		 			 	 	 		 		 	
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		   	 			  		 			 	 	 		 		 	
        If verbose = False your code should not generate ANY output.  		  	   		   	 			  		 			 	 	 		 		 	
    :type verbose: bool  		  	   		   	 			  		 			 	 	 		 		 	
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		   	 			  		 			 	 	 		 		 	
    :type impact: float  		  	   		   	 			  		 			 	 	 		 		 	
    :param commission: The commission amount charged, defaults to 0.0  		  	   		   	 			  		 			 	 	 		 		 	
    :type commission: float  		  	   		   	 			  		 			 	 	 		 		 	
    """

    # constructor
    def __init__(self, verbose=False, impact=0.0, commission=0.0):
        """  		  	   		   	 			  		 			 	 	 		 		 	
        Constructor method  		  	   		   	 			  		 			 	 	 		 		 	
        """
        self.verbose = verbose
        self.impact = impact
        self.commission = commission
        self.learner = bl.BagLearner(learner=rt.RTLearner, kwargs={"leaf_size": 5}, bags=14, boost=False, verbose=False)

    # this method should create a QLearner, and train it for trading  		  	   		   	 			  		 			 	 	 		 		 	
    def add_evidence(
            self,
            symbol="IBM",
            sd=dt.datetime(2008, 1, 1),
            ed=dt.datetime(2009, 1, 1),
            sv=10000,
    ):
        """  		  	   		   	 			  		 			 	 	 		 		 	
        Trains your strategy learner over a given time frame.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
        :param symbol: The stock symbol to train on  		  	   		   	 			  		 			 	 	 		 		 	
        :type symbol: str  		  	   		   	 			  		 			 	 	 		 		 	
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		   	 			  		 			 	 	 		 		 	
        :type sd: datetime  		  	   		   	 			  		 			 	 	 		 		 	
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		   	 			  		 			 	 	 		 		 	
        :type ed: datetime  		  	   		   	 			  		 			 	 	 		 		 	
        :param sv: The starting value of the portfolio  		  	   		   	 			  		 			 	 	 		 		 	
        :type sv: int  		  	   		   	 			  		 			 	 	 		 		 	
        """

        # add your code to do learning here


        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        prices = prices_all[symbol]  # only portfolio symbols
        prices_SPY = prices_all["SPY"]  # only SPY, for comparison later

        prices.fillna(method='ffill', inplace=True)  # fill forward
        prices.fillna(method='bfill', inplace=True)  # fill backward
        lookback = 14
        # lookback=14
        # ndays=2
        # indicators
        df_m = ind.calculate_momentum(prices, lookback)
        df_s = ind.calculate_price_sma_ratio(prices, lookback)
        df_b = ind.calculate_bbp(prices, lookback)
        ind_df = pd.concat((df_m, df_s, df_b), axis=1)
        ind_df.fillna(0, inplace=True)
        ind_df = ind_df[:-2]
        X_train = ind_df.values
        # print(prices)
        Y_train = []
        YBUY = 0.016
        YSELL = -0.016
        for i in range(len(prices)-2):
            price_ratio = (prices.iloc[i + 2] / prices.iloc[i]) -1 # price ratio , next to today
            if price_ratio > (YBUY):
                # buy
                Y_train.append(1)
            elif price_ratio < (YSELL):
                # sell
                Y_train.append(-1)
            else:
                Y_train.append(0)

        Y_train = np.array(Y_train)
        self.learner.add_evidence(X_train, Y_train)
        if self.verbose:
            print(volume)
        return Y_train

    # this method should use the existing policy and test it against new data  		  	   		   	 			  		 			 	 	 		 		 	
    def testPolicy(
            self,
            symbol="IBM",
            sd=dt.datetime(2009, 1, 1),
            ed=dt.datetime(2010, 1, 1),
            sv=10000,

    ):
        """  		  	   		   	 			  		 			 	 	 		 		 	
        Tests your learner using data outside of the training data  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
        :param symbol: The stock symbol that you trained on on  		  	   		   	 			  		 			 	 	 		 		 	
        :type symbol: str  		  	   		   	 			  		 			 	 	 		 		 	
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		   	 			  		 			 	 	 		 		 	
        :type sd: datetime  		  	   		   	 			  		 			 	 	 		 		 	
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		   	 			  		 			 	 	 		 		 	
        :type ed: datetime  		  	   		   	 			  		 			 	 	 		 		 	
        :param sv: The starting value of the portfolio  		  	   		   	 			  		 			 	 	 		 		 	
        :type sv: int  		  	   		   	 			  		 			 	 	 		 		 	
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating  		  	   		   	 			  		 			 	 	 		 		 	
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.  		  	   		   	 			  		 			 	 	 		 		 	
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to  		  	   		   	 			  		 			 	 	 		 		 	
            long so long as net holdings are constrained to -1000, 0, and 1000.  		  	   		   	 			  		 			 	 	 		 		 	
        :rtype: pandas.DataFrame  		  	   		   	 			  		 			 	 	 		 		 	
        """

        lookback = 14
        sym = [symbol]

        # your code should return the same sort of data  		  	   		   	 			  		 			 	 	 		 		 	
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY  		  	   		   	 			  		 			 	 	 		 		 	
        prices = prices_all[sym]  # only portfolio symbols
        prices_SPY = prices_all["SPY"]  # only SPY, for comparison later

        prices.fillna(method='ffill', inplace=True)  # fill forward
        prices.fillna(method='bfill', inplace=True)  # fill backward

        # indicators
        df_m = ind.calculate_momentum(prices, lookback)
        df_s = ind.calculate_price_sma_ratio(prices, lookback)
        df_b = ind.calculate_bbp(prices, lookback)
        ind_df = pd.concat((df_m,df_s,df_b), axis=1)
        ind_df.fillna(0,inplace = True)

        X_test = ind_df.values

        #test y
        Y_test = self.learner.query(X_test)

        trades = prices.copy()
        trades.iloc[:] = 0

        holding =0
        for i in range(0, len(prices) - 1):
            if Y_test[i] > 0:
                Y_test[i] = 1
                #long
                if holding == 0:
                    holding = holding + 1000
                    trades.iloc[i, 0] = 1000
                elif holding == -1000:
                    holding = holding + 2000
                    trades.iloc[i, 0] = 2000

            elif Y_test[i] < 0:
                Y_test[i] =-1
                #short
                if holding == 0:
                    holding = holding - 1000
                    trades.iloc[i, 0] = -1000
                elif holding == 1000:
                    holding = holding - 2000
                    trades.iloc[i, 0] = -2000
            else:
                Y_test[i] = 0


        if self.verbose:
            print(type(trades))  # it better be a DataFrame!  		  	   		   	 			  		 			 	 	 		 		 	
        if self.verbose:
            print(trades)
        if self.verbose:
            print(prices_all)
        return trades


if __name__ == "__main__":
    print("One does not simply think up a strategy")

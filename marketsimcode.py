""""""  		  	   		   	 			  		 			 	 	 		 		 	
"""MC2-P1: Market simulator.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
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
import os  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
import numpy as np

import pandas as pd  		  	   		   	 			  		 			 	 	 		 		 	
from util import get_data, plot_data  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
def author():
    return 'samoozegar3'

def compute_portvals(  		  	   		   	 			  		 			 	 	 		 		 	
    orders_df,
    start_val=1000000,  		  	   		   	 			  		 			 	 	 		 		 	
    commission=9.95,  		  	   		   	 			  		 			 	 	 		 		 	
    impact=0.005,  		  	   		   	 			  		 			 	 	 		 		 	
):  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    Computes the portfolio values.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
    :param orders_file: dataframe 		  	   		   	 			  		 			 	 	 		 		 	
    :type orders_file: pandas dataframe 		  	   		   	 			  		 			 	 	 		 		 	
    :param start_val: The starting value of the portfolio  		  	   		   	 			  		 			 	 	 		 		 	
    :type start_val: int  		  	   		   	 			  		 			 	 	 		 		 	
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		   	 			  		 			 	 	 		 		 	
    :type commission: float  		  	   		   	 			  		 			 	 	 		 		 	
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		   	 			  		 			 	 	 		 		 	
    :type impact: float  		  	   		   	 			  		 			 	 	 		 		 	
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		   	 			  		 			 	 	 		 		 	
    :rtype: pandas.DataFrame  		  	   		   	 			  		 			 	 	 		 		 	
    """

 
    # print ('orders_df', orders_df)

    #get the start and end dates for all the orders
    start_date = orders_df.index.min()
    end_date = orders_df.index.max()
    sym = [orders_df.columns[0]]

    #step one- get prices dataframe with [date symbols cash]
    prices = get_data(sym, pd.date_range(start_date, end_date))
    prices = prices[sym]

    prices.fillna(method='ffill', inplace=True) #fill forward
    prices.fillna(method='bfill', inplace=True) #fill backward

    prices['Cash'] = 1 # create a new column cash with

    trades = prices.copy() # make a copy of prices dataframe

    trades = trades.applymap(lambda x: 0) #all values in trades dataframe would become zero
    trades = trades.sort_index()
    #populate trades dataframe

    for i,row in orders_df.iterrows():
        symbol= orders_df.columns[0]
        shares = row[symbol]
        if shares >0: #buy
            trades.ix[i , symbol] = trades.ix[i , symbol] + abs(shares)#if 'BUY' number of shares would increase
            trades.ix[i, 'Cash'] = trades.ix[i, 'Cash'] - ((prices.ix[i, symbol] * abs(shares) * (1 + impact)) + commission) # if 'BUY' cash would decrease
        elif shares < 0: #sell
            trades.ix[i, symbol] = trades.ix[i, symbol] - abs(shares)#if 'SELL' number of shares would decrease
            trades.ix[i, 'Cash'] = trades.ix[i, 'Cash'] + (
                        prices.ix[i, symbol] * abs(shares) * (1 - impact) ) - commission # if 'SELL' cash would increase but we have to pay commossion
    holdings = trades.copy()

    for i in range(1, len(holdings)):
        holdings.iloc[i] = holdings.iloc[i] + holdings.iloc[i-1] #current row + previous row

    values = holdings.multiply(prices)
    values = values.dropna()
    values['Cash'] = values['Cash'] + start_val


    portvals = values.sum(axis=1)

    return portvals  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
def test_code():  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    Helper function to test code  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    # this is a helper function you can use to test your code  		  	   		   	 			  		 			 	 	 		 		 	
    # note that during autograding his function will not be called.  		  	   		   	 			  		 			 	 	 		 		 	
    # Define input parameters  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	

    sv = 1000000  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
    # Process orders  		  	   		   	 			  		 			 	 	 		 		 	
    portvals = compute_portvals(orders_df, start_val=sv)
    if isinstance(portvals, pd.DataFrame):  		  	   		   	 			  		 			 	 	 		 		 	
        portvals = portvals[portvals.columns[0]]  # just get the first column  		  	   		   	 			  		 			 	 	 		 		 	
    else:  		  	   		   	 			  		 			 	 	 		 		 	
        "warning, code did not return a DataFrame"  		  	   		   	 			  		 			 	 	 		 		 	
    # print('portvals', portvals)
    # Get portfolio stats  		  	   		   	 			  		 			 	 	 		 		 	
    # Here we just fake the data. you should use your code from previous assignments.  		  	   		   	 			  		 			 	 	 		 		 	
    start_date = dt.datetime(2008, 1, 1)  		  	   		   	 			  		 			 	 	 		 		 	
    end_date = dt.datetime(2008, 6, 1)  		  	   		   	 			  		 			 	 	 		 		 	
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [  		  	   		   	 			  		 			 	 	 		 		 	
        0.2,  		  	   		   	 			  		 			 	 	 		 		 	
        0.01,  		  	   		   	 			  		 			 	 	 		 		 	
        0.02,  		  	   		   	 			  		 			 	 	 		 		 	
        1.5,  		  	   		   	 			  		 			 	 	 		 		 	
    ]  		  	   		   	 			  		 			 	 	 		 		 	
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [  		  	   		   	 			  		 			 	 	 		 		 	
        0.2,  		  	   		   	 			  		 			 	 	 		 		 	
        0.01,  		  	   		   	 			  		 			 	 	 		 		 	
        0.02,  		  	   		   	 			  		 			 	 	 		 		 	
        1.5,  		  	   		   	 			  		 			 	 	 		 		 	
    ]  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
    # Compare portfolio against $SPX  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Date Range: {start_date} to {end_date}")  		  	   		   	 			  		 			 	 	 		 		 	
    print()  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")  		  	   		   	 			  		 			 	 	 		 		 	
    print()  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Cumulative Return of Fund: {cum_ret}")  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Cumulative Return of SPY : {cum_ret_SPY}")  		  	   		   	 			  		 			 	 	 		 		 	
    print()  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")  		  	   		   	 			  		 			 	 	 		 		 	
    print()  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")  		  	   		   	 			  		 			 	 	 		 		 	
    print()  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Final Portfolio Value: {portvals[-1]}")  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
if __name__ == "__main__":  		  	   		   	 			  		 			 	 	 		 		 	
    test_code()  		  	   		   	 			  		 			 	 	 		 		 	

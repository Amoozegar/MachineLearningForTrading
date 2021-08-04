import pandas as pd
import datetime as dt
from util import get_data, plot_data
import matplotlib.pyplot as plt

def author():
    return 'samoozegar3'

def calculate_sma(price_df, lookback = 14):
    """
    function to calculate SMA(simple moving average)
    inputs
    df: dataframe containing historical daily returns
    """
    sma = price_df.rolling( window=lookback, min_periods=lookback).mean()
    return sma

def calculate_rolling_std(price_df, lookback = 14):
    rolling_std = price_df.rolling(window=lookback, min_periods=lookback).std()
    return rolling_std

def calculate_bbp_topband(price_df, lookback = 14):
    sma = calculate_sma(price_df, lookback)
    top_band = sma + (2 * calculate_rolling_std(price_df, lookback))
    return top_band

def calculate_bbp_bottomband(price_df, lookback = 14):
    sma = calculate_sma(price_df, lookback)
    bottom_band = sma - (2 * calculate_rolling_std(price_df, lookback))
    return bottom_band

def calculate_bbp(price_df, lookback = 14):
    top_band = calculate_bbp_topband(price_df, lookback)
    bottom_band = calculate_bbp_bottomband(price_df, lookback)
    bbp = (price_df - bottom_band) / (top_band - bottom_band)
    return bbp

def calculate_momentum(price_df, lookback = 14):
    momentum = price_df / price_df.shift(lookback-1) - 1
    return momentum

def calculate_expma(price_df, lookback = 14):
    """Takes a df and number of days and returns an exponential moving average"""
    expma = price_df.ewm(span=lookback, min_periods=lookback, adjust=False).mean()
    # print ('expma',expma)
    return expma


def calculate_macd(price_df, period_long=26, period_short=12, period_signal=9):
    ema_short = calculate_expma(price_df, period_short)
    ema_long = calculate_expma(price_df, period_long)
    macd = ema_short - ema_long
    signal_line = macd.ewm(ignore_na=False, min_periods=0, com=period_signal,adjust=True).mean()
    return macd, signal_line

def calculate_price_sma_ratio(price_df, lookback = 14):
    sma = calculate_sma(price_df)
    psma_ratio = price_df/sma
    return psma_ratio


def main():
    #generate the charts in here
    lookback= 14
    symbol = ['JPM']  # the stock symbol to act on
    sd = dt.datetime(2008,1,1)    #datetime object representing start date
    ed = dt.datetime (2009,12,31)     #datetime object representing end date
    # sv =      #start value of the portfolio
    prices = get_data(symbol, pd.date_range(sd, ed))

    prices = prices[symbol]
    prices.fillna(method='ffill', inplace=True) #fill forward
    prices.fillna(method='bfill', inplace=True) #fill backward

    prices = prices/prices.iloc[0] #normalize prices
    prices.dropna(inplace = True)
    # -----------------------------------charts-------------------------------
    #calculate bbp%
    bbp = calculate_bbp(prices, lookback)
    top_band = calculate_bbp_topband(prices, lookback)
    bottom_band = calculate_bbp_bottomband(prices, lookback)

    fig1, ax = plt.subplots()
    ax.plot(prices, label = 'prices')
    ax.plot(bbp, label = 'bbp%')
    ax.plot(top_band, label = 'top band')
    ax.plot(bottom_band, label = 'bottom band')
    plt.title('Normalized historical prices and Bolinger bands')
    ax.legend()
    plt.xticks(fontsize=7)
    plt.xlabel('Date')
    fig1.savefig('bbp.png')

    #caclulate momentum
    momentum = calculate_momentum(prices, lookback)
    fig2, ax = plt.subplots()
    ax.plot(prices, label='prices')
    ax.plot(momentum, label='momentum')
    plt.title('Normalized historical prices and momentum')
    plt.legend()
    plt.xticks(fontsize=7)
    plt.xlabel('Date')
    fig2.savefig('momentum.png')

    #calculate sma
    sma = calculate_sma(prices, lookback)
    sma_ratio = prices/sma
    fig3, ax = plt.subplots()
    ax.plot(prices, label='Prices')
    ax.plot(sma, label='Simple moving average')
    ax.plot(sma_ratio, label='Price/SMA ratio')
    plt.title('Normalized historical prices, and simple moving average')
    plt.xticks(fontsize=7)
    ax.legend()
    plt.xlabel('Date')
    fig3.savefig('SMA.png')


    #caculate macd
    macd, signal_line = calculate_macd(prices)
    fig4, ax = plt.subplots()
    ax.plot(prices, label='prices')
    ax.plot(macd, label='MACD')
    ax.plot(signal_line, label = 'signal line')
    plt.title('Normalized historical price and MACD')
    ax.legend()
    plt.xticks(fontsize=7)
    plt.xlabel('Date')
    fig4.savefig('MACD.png')


    #caculate exponential moving average
    expma = calculate_expma(prices, lookback)
    fig5, ax = plt.subplots()
    ax.plot(prices, label='prices')
    ax.plot(expma, label='exponential moving average')
    plt.title('Normalized historical price and exponential moving average')
    plt.xticks(fontsize=7)
    ax.legend()
    plt.xlabel('Date')
    fig5.savefig('EMA.png')

if __name__ == "__main__":
    main()




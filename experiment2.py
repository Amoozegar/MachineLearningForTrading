import datetime as dt
import util as ut
import StrategyLearner as st
import pandas as pd
import marketsimcode as mc
import matplotlib.pyplot as plt


def author():
    return 'samoozegar3'

def create_experiment2(symbol, sd, ed, sv, verbose):
    commission = 9.95
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    symbol = ['JPM']
    dates = dates = pd.date_range(sd, ed)
    prices_all = ut.get_data(symbol, dates)
    prices = prices_all[symbol]

    # impact 0.05
    learner = st.StrategyLearner(verbose=False, impact=0.05, commission=9.95 )
    learner.add_evidence(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    test_result = learner.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    port_val_1 = mc.compute_portvals(test_result, 100000, commission, 0.05)
    # calculate statistics
    daily_returns_1 = (port_val_1 / port_val_1.shift(1)) - 1
    daily_returns_1 = daily_returns_1[1:]
    cum_return_1 = (port_val_1.iloc[-1] / port_val_1.iloc[0]) - 1
    avg_daily_return_1 = daily_returns_1.mean()
    std_daily_return_1 = daily_returns_1.std()

    if verbose:
        print('average daily return(impact = 0.05) ', round(avg_daily_return_1, 4))
        print('standard deviation of daily return(impact = 0.05) ', round(std_daily_return_1, 4))
        print('cumulative return(impact = 0.05) ', round(cum_return_1, 4))

    # impact 0.005
    learner = st.StrategyLearner(verbose=False, impact=0.005)
    learner.add_evidence(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    test_result = learner.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    port_val_2 = mc.compute_portvals(test_result, 100000, commission, 0.005)

    # calculate statistics
    daily_returns_2 = (port_val_2 / port_val_2.shift(1)) - 1
    daily_returns_2 = daily_returns_2[1:]
    cum_return_2 = (port_val_2.iloc[-1] / port_val_2.iloc[0]) - 1
    avg_daily_return_2 = daily_returns_2.mean()
    std_daily_return_2 = daily_returns_2.std()

    if verbose:
        print('average daily return(impact = 0.005) ', round(avg_daily_return_2, 4))
        print('standard deviation of daily return(impact = 0.005) ', round(std_daily_return_2, 4))
        print('cumulative return(impact = 0.005) ', round(cum_return_2, 4))

    # impact 0.0005
    learner = st.StrategyLearner(verbose=False, impact=0.0005)
    learner.add_evidence(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    test_result = learner.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    port_val_3 = mc.compute_portvals(test_result, 100000, commission, 0.0005)

    # calculate statistics
    daily_returns_3 = (port_val_3 / port_val_3.shift(1)) - 1
    daily_returns_3 = daily_returns_3[1:]
    cum_return_3 = (port_val_3.iloc[-1] / port_val_3.iloc[0]) - 1
    avg_daily_return_3 = daily_returns_3.mean()
    std_daily_return_3 = daily_returns_3.std()

    if verbose:
        print('average daily return(impact = 0.0005) ', round(avg_daily_return_3, 4))
        print('standard deviation of daily return(impact = 0.0005) ', round(std_daily_return_3, 4))
        print('cumulative return(impact = 0.0005) ', round(cum_return_3, 4))

    # visualization
    norm_port_val_1 = port_val_1 / port_val_1[0]
    norm_port_val_2 = port_val_2 / port_val_2[0]
    norm_port_val_3 = port_val_3 / port_val_3[0]

    fig, ax = plt.subplots()
    ax.plot(norm_port_val_1, color="g", label="impact: 0.05")
    ax.plot(norm_port_val_2, color="r", label="impact: 0.005")
    ax.plot(norm_port_val_3, color="b", label="impact: 0.0005")
    ax.legend()
    plt.title('Experiment 2')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value')
    plt.xticks(fontsize=7)
    plt.savefig('exp2.png')
    # plt.show()

if __name__=="__main__":

    symbol = 'JPM'
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000
    verbose= False
    create_experiment2(symbol, sd, ed, sv, verbose)








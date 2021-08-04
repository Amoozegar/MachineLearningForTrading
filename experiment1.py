import util as ut
import StrategyLearner as sl
import ManualStrategy as ms
import pandas as pd
import marketsimcode as mc
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt


def author():
    return 'samoozegar3'

def create_experiment1(symbol, sd, ed, sv, verbose):
    commission = 9.95
    impact = 0.005
    symbol = symbol

    sd = sd
    ed = ed
    sv = sv
    dates = pd.date_range(sd, ed)

    # strategy learner
    learner = sl.StrategyLearner(verbose=False, impact=impact, commission=commission)
    learner.add_evidence(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)

    # strategy learner : in-sample
    df_trades = learner.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    port_val_st = mc.compute_portvals(df_trades, 100000, commission, impact)

    # strategy learner : out-sample
    df_trades_outsample = learner.testPolicy(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31),
                                             sv=100000)
    port_val_st_outsample = mc.compute_portvals(df_trades_outsample, 100000, commission, impact)

    # Benchmark : insample
    benchmark = df_trades.copy()  # copy in-smaple dataframe
    benchmark.iloc[:, 0] = 0
    benchmark.iloc[0, 0] = 1000
    benchmark_port_val = mc.compute_portvals(benchmark, 100000, commission, impact)

    # benchmark : out-sample
    bench_outsample = df_trades_outsample.copy()  # copy out-sample dataframe
    bench_outsample.iloc[:, 0] = 0
    bench_outsample.iloc[0, 0] = 1000
    bench_outsample_portval = mc.compute_portvals(bench_outsample, 100000, commission, impact)

    # ManualStrategy: in-sample
    trades = ms.testPolicy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    port_val_ms = mc.compute_portvals(trades, 100000, commission, impact)

    # manual Strategy : out-sample
    trades_outsample = ms.testPolicy(symbol='JPM', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)
    port_val_ms_outsample = mc.compute_portvals(trades_outsample, 100000, commission, impact)

    # Portfolio statistics

    # manual startegy : in-sample
    daily_returns = (port_val_ms / port_val_ms.shift(1)) - 1
    daily_returns = daily_returns[1:]
    cum_return = (port_val_ms.iloc[-1] / port_val_ms.iloc[0]) - 1
    avg_daily_return = daily_returns.mean()
    std_daily_return = daily_returns.std()
    if verbose:
        print('average daily return for manual strategy(in-sample)', round(avg_daily_return, 4))
        print('standard deviation of daily return for manual strategy(in-sample) ', round(std_daily_return, 4))
        print('cumulative return for manual strategy(in-sample) ', round(cum_return, 4))

    # manual startegy : out-sample
    daily_returns_os = (port_val_ms_outsample / port_val_ms_outsample.shift(1)) - 1
    daily_returns_os = daily_returns_os[1:]
    cum_return_os = (port_val_ms_outsample.iloc[-1] / port_val_ms_outsample.iloc[0]) - 1
    avg_daily_return_os = daily_returns_os.mean()
    std_daily_return_os = daily_returns_os.std()
    if verbose:
        print('\naverage daily return for manual strategy(out-sample)', round(avg_daily_return_os, 4))
        print('standard deviation of daily return for manual strategy(out-sample) ', round(std_daily_return_os, 4))
        print('cumulative return for manual strategy(out-sample) ', round(cum_return_os, 4))


    # StrategyLearner : in sample
    daily_return_st = (port_val_st / port_val_st.shift(1)) - 1
    daily_return_st = daily_return_st[1:]
    cum_return_st = (port_val_st.iloc[-1] / port_val_st.iloc[0]) - 1
    avg_daily_return_st = daily_return_st.mean()
    std_daily_return_st = daily_return_st.std()
    if verbose:
        print('\naverage daily return for strategy learner(in-sample)', round(avg_daily_return_st, 4))
        print('standard deviation of daily return for strategy learner(in-sample) ', round(std_daily_return_st, 4))
        print('cumulative return for strategy learner(in-sample) ', round(cum_return_st, 4))


    # Strategy learner out-sample
    st_daily_return_os = (port_val_st_outsample / port_val_st_outsample.shift(1)) - 1
    st_daily_return_os = st_daily_return_os[1:]
    st_cum_return_os = (port_val_st_outsample.iloc[-1] / port_val_st_outsample.iloc[0]) - 1
    avg_daily_return_st_os = st_daily_return_os.mean()
    std_daily_return_st_os = st_daily_return_os.std()
    if verbose:
        print('\naverage daily return for strategy learner(out-sample)', round(avg_daily_return_st_os, 4))
        print('standard deviation of daily return for strategy learner(out-sample) ', round(std_daily_return_st_os, 4))
        print('cumulative return for strategy learner(out-sample) ', round(st_cum_return_os, 4))


    # Plotting charts
    normalized_val_ms = port_val_ms / port_val_ms[0]
    normalized_val_benchmark = benchmark_port_val/benchmark_port_val[0]
    normalized_val_st = port_val_st / port_val_st[0]
    fig1, ax = plt.subplots()
    ax.plot(normalized_val_ms, color="red", label="Manual Strategy")
    ax.plot(normalized_val_benchmark, color="green", label='Benchmark')
    ax.plot(normalized_val_st, color="black", label='Strategy Learner')
    plt.title("Experiment 1: in sample")
    plt.xlabel("Date")
    plt.ylabel("Normalized prices")
    plt.legend()
    plt.xticks(fontsize=7)
    fig1.savefig('exp1_1.png')

    norm_port_val_ms_outsample  = port_val_ms_outsample / port_val_ms_outsample[0]
    norm_bench_outsample_portval = bench_outsample_portval / bench_outsample_portval[0]
    norm_port_val_st_outsample = port_val_st_outsample / port_val_st_outsample[0]
    fig2, ax = plt.subplots()
    ax.plot(norm_port_val_ms_outsample, color="red", label="Manual Strategy")
    ax.plot(norm_bench_outsample_portval, color="green", label='Benchmark')
    ax.plot(norm_port_val_st_outsample, color="black", label='Strategy Learner')
    plt.title("Experiment 1: out sample")
    plt.xlabel("Date")
    plt.ylabel("Normalized prices")
    plt.legend()
    plt.xticks(fontsize=7)
    fig2.savefig('exp1_2.png')

    fig3, ax = plt.subplots()
    ax.plot(normalized_val_ms, color="red", label="Manual Strategy")
    ax.plot(normalized_val_st, color="black", label='Strategy Learner')
    plt.title("Experiment 1: in-sample-comparison between Manual and strategy learner")
    plt.xlabel("Date")
    plt.ylabel("Normalized prices")
    plt.legend()
    plt.xticks(fontsize=7)
    fig3.savefig('exp1_3.png')

if __name__=="__main__":

    symbol = 'JPM'
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000
    verbose= False
    create_experiment1(symbol, sd, ed, sv, verbose)









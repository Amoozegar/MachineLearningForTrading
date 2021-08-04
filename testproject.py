import StrategyLearner as sl
import ManualStrategy as ms
import experiment1 as exp1
import experiment2 as exp2
import datetime as dt
import sys

def author():
    return 'samoozegar3'

def main(argv):

    verbose = False
    if len(argv) >1:
        if argv[1]=='-print_to_screen':
            verbose = True
    symbol = 'JPM'
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000
    ms.plot_ManualStrategy(symbol, sd, ed, sv, verbose)
    exp1.create_experiment1(symbol, sd, ed, sv, verbose)
    exp2.create_experiment2(symbol, sd, ed, sv, verbose)


if __name__=="__main__":
    main(sys.argv)














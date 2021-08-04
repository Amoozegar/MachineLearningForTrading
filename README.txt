Copy testproject.py, indicators.py, ManualStrategy.py, marketsimcode.py, StrategyLearner.py, BagLearner.py, RTLearner.py, experiment1.py, and experiment2.py  in the same directory as util.py and other data files used in util.py.


- to generate all the results for manual learner, experiment1 and experiment2 with printed statistics to the console/screen/terminal run the following command:

PYTHONPATH=../:. python testproject.py -print_to_screen

This command will save all the charts in the same directory as testproject.py, and prints statistics in the console.


- to generate all the results for manual learner, experiment1 and experiment2 without printing statistics run the following command:

PYTHONPATH=../:. python testproject.py

This command will save all the charts in the same directory as testproject.py without printing anything in the console.


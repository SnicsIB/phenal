"""
Prints probability of getting x or more distant value from mean

Usage:
python bincalc.py x n

Args:
x -- number of events
n -- total trials

Example:
python bincalc.py 1400 2772
"""
from sys import argv
from scipy.stats import binom


try:
    x = int(argv[1])
    n = int(argv[2])
    x = min(x, n - x)+1
    res = 0.0
    for i in range(x):
        res += binom.pmf(i, n, 0.5)
    print 2*res
except ValueError:
    print "Arguments are not integers"
except IndexError:
    print "Not enough arguments"

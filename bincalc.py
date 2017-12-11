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
    if 2*x == n+2:  # do not count middle value twice
        print 2 * res - binom.pmf(x-1, n, 0.5)
    else:
        print 2 * res
except ValueError:
    print "Arguments are not integers"
except IndexError:
    print "Not enough arguments"

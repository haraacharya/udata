"""
This is the "update_formulae" module.

It performs a number of weighted updates that are needed for streaming learning, e.g.,

>>> convex_combination(10,20,0.3)
13.0

It also hosts certain decision formulae.
"""

import numpy as np 


def decision_rule(score, threshhold=0.99, two_sided=True):
    """

    :param score: a score, assumed normalised (between 0 and 1) representing anomalousness
    :param threshold: a user-specified threshold above which an alert should be raised
    :param two_sided: if True, we flag anomalies that are either smaller than 1-threshold or larger than threhsold
    :return: a boolean flag

    >>> decision_rule(score=0.9)
    False
    >>> decision_rule(score=0.95, threshold=0.9)
    True
    >>> decision_rule(score=0.0001, threshold=0.99)
    True
    >>> decision_rule(score=0.001, two_sided=False)
    False
    """
    if two_sided:
        ans = np.logical_or(score < 1-threshhold, score > threshhold)
    else:
        ans = score > threshhold

    return ans

def rolling_window_update():
    pass

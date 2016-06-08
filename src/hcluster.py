"""
Module hcluster
Basic hierarchial clustering in pure Python
"""


import math


def euclidian(a, b):
    """ Euclidian distance in N-space """
    return math.sqrt(sum((x - y) ** 2 for (x, y) in zip(a, b)))

"""
Module hcluster
Basic hierarchial clustering in pure Python
"""


import math


def euclidian(a, b):
    """ Euclidian distance in N-space """
    return math.sqrt(sum((x - y) ** 2 for (x, y) in zip(a, b)))


def distance_matrix(data, dist):
    """ Distance matrix (all-to-all) """
    m = []
    for elem1 in data:
        m.append([])
        for elem2 in data:
            m[-1].append(dist(elem1, elem2))
    return m


def cluster(data, dist=None):
    dist = dist or euclidian
    m = distance_matrix(data, dist)

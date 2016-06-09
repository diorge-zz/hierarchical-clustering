"""
Module hcluster
Basic hierarchial clustering in pure Python
"""


import math


def euclidian(a, b):
    """ Euclidian distance in N-space """
    return math.sqrt(sum((x - y) ** 2 for (x, y) in zip(a, b)))


def distance_matrix(data, dist):
    """ Distance matrix (all-to-all), dictionary form """
    return {(elem1, elem2): dist(elem1, elem2)
            for elem1 in data
            for elem2 in data
            if elem1 != elem2}


class HashableSet(set):
    """ Extension of set to allow XOR hashing and unpacked init """

    def __init__(self, *args):
        set.__init__(self, args)

    def __hash__(self):
        return hash(tuple(sorted(self)))


class Hierarchy(object):
    """ Hierarchial clustering """

    def __init__(self, data, matrix):
        """
        Constructs the Hierarchy by the given distance matrix
        Copies the data list
        """
        self._data = data[:]
        self._matrix = matrix

    def pair(self, elem1, elem2):
        """ Pairs two elements of the current data set in a cluster """
        n = HashableSet(elem1, elem2)
        for elem in self._data:
            if elem not in n:
                avg = ((self._matrix[(elem, elem1)] +
                       self._matrix[(elem, elem2)]) / 2)
                self._matrix[(elem, n)] = avg
                self._matrix[(n, elem)] = avg
                del self._matrix[(elem, elem1)]
                del self._matrix[(elem, elem2)]
                del self._matrix[(elem1, elem)]
                del self._matrix[(elem2, elem)]
        del self._matrix[(elem1, elem2)]
        del self._matrix[(elem2, elem1)]
        del self._data[self._data.index(elem1)]
        del self._data[self._data.index(elem2)]
        self._data.append(n)

    def next(self):
        """ Finds the next lowest distance """
        m = float('inf')
        v = None
        for e1, e2 in self._matrix:
            if e1 != e2 and self._matrix[(e1, e2)] < m:
                m = self._matrix[(e1, e2)]
                v = (e1, e2)
        return v

    def cluster(self):
        """ Clusters the data set until its fully clustered """
        while len(self._data) > 1:
            e1, e2 = self.next()
            self.pair(e1, e2)

    def setrepr(self):
        """ Recursive set representation """
        return self._data[0]


def cluster(data, dist=None):
    """
    Hierarchically clusters the data set, using the given dist function
    """
    dist = dist or euclidian
    m = distance_matrix(data, dist)
    h = Hierarchy(data, m)
    h.cluster()
    return h

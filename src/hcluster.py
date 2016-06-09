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


def min_index(matrix):
    """
    Gives the (i, j) index of the minimum value in the matrix
    Ignores the main diagonal (expected values of zero)
    """
    m = float('inf')
    v = None
    for e1, e2 in matrix:
        if e1 != e2 and matrix[(e1, e2)] < m:
            m = matrix[(e1, e2)]
            v = (e1, e2)
    return v


class HashableSet(set):

    def __init__(self, *args):
        set.__init__(self, args)

    def __hash__(self):
        h = 17
        for x in self:
            h = h ^ hash(x)
        return h


class Hierarchy(object):
    
    def __init__(self, data, matrix):
        self._data = data[:]
        self._matrix = matrix

    def pair(self, elem1, elem2):
        n = HashableSet(elem1, elem2)
        for elem in self._data:
            if elem not in n:
                avg = (self._matrix[(elem, elem1)] + self._matrix[(elem, elem2)]) / 2
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

    def cluster(self):
        while len(self._data) > 1:
            e1, e2 = min_index(self._matrix)
            self.pair(e1, e2)
        

    def setrepr(self):
        return self._data[0]


def cluster(data, dist=None):
    dist = dist or euclidian
    m = distance_matrix(data, dist)
    h = Hierarchy(data, m)
    h.cluster()
    return h

"""
Unit tests for the hcluster module
"""


import hcluster
import math
from unittest import TestCase


class TestHCluster(TestCase):
    
    def test_base_call(self):
        """ Basic call - assumes Euclidian Distance """
        data = [(5, 5), (5, 6), (1, 1), (0, 0)]
        c = hcluster.cluster(data)
        # expected structure:
        #       |-------------|
        #   |-------|         |
        #   |       |     |-------|
        # (0, 0) (1, 1) (5, 5) (5, 6)
        expected = set(set((0, 0), (1, 1)), set((5, 5), (5, 6)))
        assert expected == c.setrepr()

    def test_cust_func(self):
        """ Call passing a custom distance function """
        data = [(5, 0), (0, 0), (1, 2)]
        yDist = lambda a, b: abs(a[1] - b[1])
        c = hcluster.cluster(data, yDist)
        expected = set(set((5, 0), (0, 0)), (1, 2))
        assert expected == c.setrepr()

    def test_distance_matrix(self):
        data = [(5, 5), (5, 6), (4, 4)]
        m = hcluster.distance_matrix(data, hcluster.euclidian)
        assert m[0] == [0, 1, math.sqrt(2)]
        assert m[1] == [1, 0, math.sqrt(5)]
        assert m[2] == [math.sqrt(2), math.sqrt(5), 0]

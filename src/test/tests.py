"""
Unit tests for the hcluster module
"""


import hcluster
from hcluster import HashableSet as hset
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
        expected = hset(hset((0, 0), (1, 1)), hset((5, 5), (5, 6)))
        assert expected == c.setrepr()

    def test_cust_func(self):
        """ Call passing a custom distance function """
        data = [(5, 0), (0, 0), (1, 2)]
        yDist = lambda a, b: abs(a[1] - b[1])
        c = hcluster.cluster(data, yDist)
        expected = hset(hset((5, 0), (0, 0)), (1, 2))
        assert expected == c.setrepr()

    def test_distance_matrix(self):
        data = [(5, 5), (5, 6), (4, 4)]
        m = hcluster.distance_matrix(data, hcluster.euclidian)
        assert m[((5, 5), (5, 6))] == 1
        assert m[((4, 4), (5, 6))] == math.sqrt(5)
        assert m[((5, 5), (4, 4))] == math.sqrt(2)

import math

# Some utility functions

def add_elements(a, b):
    return tuple([sum(x) for x in zip(a, b)])

def subtract_elements(a, b):
    return tuple([x[0] - x[1] for x in zip(a, b)])

def average_elements(a, b):
    return tuple([sum(x) / 2 for x in zip(a, b)])

def grid_distance(a, b):
    return sum([abs(x[0] - x[1]) for x in zip(a, b)])


def in_bounds(value, dimensions):
    """Check that a value is within bounds - IE 0 <= value[x] < dimensions[x]"""
    return all([0 <= x[0] and x[0] < x[1] for x in zip(value, dimensions)])

def sigmoid(x):
    return 1 / (1 + math.exp(-x))
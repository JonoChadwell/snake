from ai import *

def test_shortest_path():
    assert shortest_path(
        4, 4, (0,0), (3,3), []
    ) is not None

    assert shortest_path(
        4, 4, (0,0), (3,0), []
    ) == [(1,0), (1,0), (1,0)]

    assert shortest_path(
        4, 4, (0,0), (3,0), [(2,0), (2,1), (2,2), (2,3)]
    ) is None

def test_flood_distance():
    assert flood_distance(4, 4, (1,1), [(0,0)]) == 2
    assert flood_distance(4, 4, (0,0), [(0,0), (1,0)]) == 0
    assert flood_distance(4, 4, (1,1), [(0,0), (1,0), (1,1), (1,2), (1,3), (2,3), (3,3)]) == 4
    assert flood_distance(4, 4, (2,3), [(0,0), (1,0), (1,1), (1,2), (1,3), (2,3), (3,3)]) == 5

def test_supergrid_factor():
    assert supergrid_factor(4,4, []) == 4
    assert supergrid_factor(8,9, []) == 16
    assert supergrid_factor(8,9, [(5,5)]) == 15
    assert supergrid_factor(8,8, [(3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7)]) == 8

def test_navigation_factor():
    a = navigation_factor(4,4,[(0,0)])
    b = navigation_factor(4,4,[(2,2)])

    # Test that snake in middle is more navigable than snake on edge
    assert a > 0
    assert a > b

    assert navigation_factor(4,4,[(2,2), (2,3), (3,3)]) > 0

    # Test that snake on wall is more navigable than blocking snake
    c = navigation_factor(8,8, [(0,0), (1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7)])
    d = navigation_factor(8,8, [(0,0), (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(7,1)])
    assert d < c
    
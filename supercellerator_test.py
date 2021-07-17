from supercellerator import *

import pytest

def test_supercell():
    assert supercell((5,5)) == (4,4)
    assert supercell((0,1)) == (0,0)

def test_supercellerate():
    assert supercellerate([(0,0), (1,0), (2,0)]) == [((0,0), [(1,0), (0,0)]), ((2,0), [(2,0)])]

def test_find_path_to_goal():
    assert find_path_to_goal(10, 10, [(0,0), (2,0)], (8,0)) \
            == [(0,0), (2,0), (4,0), (6,0), (8,0)]

def test_update_path():
    assert list(update_path(10, 10, deque([(0,0), (2,0)]), (8,0))) \
            == [(0,0), (2,0), (4,0), (6,0), (8,0), (6,0), (4,0), (2,0)]
    # assert list(update_path(8, 8, deque([(4, 4), (6, 4), (6, 2), (4, 2), (6, 2), (6, 4), (6, 6), (6, 4)], )))

def test_add_to_path():
    assert list(add_to_path([(4,0), (2,0), (0,0), (2,0)], [(2,0), (2,2), (2,4)], 1)) \
            == [(4,0), (2,0), (2,2), (2,4), (2,2), (2,0), (0,0), (2,0)]

def test_clockwise_rotate():
    assert clockwise_rotate((1,2)) == (-2, 1)

def test_path_valid():
    with pytest.raises(AssertionError):
        assert_path_valid(1,1, deque([]))

    with pytest.raises(AssertionError):
        assert_path_valid(10,10, [(0,0)])

    assert_path_valid(10,10, deque([(0,0)]))
    assert_path_valid(10,10, deque([(0,0), (0,2), (0,4), (0,2)]))

    with pytest.raises(AssertionError):
        assert_path_valid(10,10, deque([(0,0), (0,2), (-2,2)]))

    with pytest.raises(AssertionError):
        assert_path_valid(10,10, deque([(0,0), (0,2), (0,2)]))

    with pytest.raises(AssertionError):
        assert_path_valid(10,10, deque([(0,0), (0,2), (0,6)]))

    assert_path_valid(8,8, deque([(0,0), (0,2), (0,4), (0,6), (0,4), (0,2)]))
    with pytest.raises(AssertionError):
        assert_path_valid(6,6, deque([(0,0), (0,2), (0,4), (0,6), (0,4), (0,2)]))

def test_clockwise_reachable():
    assert set(clockwise_reachable([(2,0), (2,2), (2,4), (2,2)], 1)) == {(4,2)}
    assert set(clockwise_reachable([(0,0), (0,2), (0,4), (0,2)], 3)) == {(-2,2)}
    assert set(clockwise_reachable([(4,4)], 0)) == {(4,6), (4,2), (2,4), (6,4)}
    assert set(clockwise_reachable([(2,4), (2,2), (2,4), (2,6)], 1)) == {(0,2), (2,0), (4,2)}
    assert set(clockwise_reachable([(2,2), (2,4)], 0)) == {(0,2), (2,0), (4,2)}

def test_reduce_path():
    start = deque([(0,0)])
    assert reduce_path(start, deque([(0,0)]), (0,0)) is start
    assert reduce_path(start, deque([(1,1)]), (0,0)) is start

    start = deque([(0,0), (2,0), (4,0), (2,0), (0,0), (0,2)])
    assert reduce_path(start, deque([(0,0), (1,0)]), (4,0)) is start
    assert reduce_path(start, deque([(0,0), (1,0)]), (0,0)) == deque([(0,0), (0,2)])

    start = deque([(0,0), (2,0), (4,0), (2,0), (2,2), (2,4), (2,2), (2,0), (0,0), (0,2)])
    assert reduce_path(start, deque([(0,0), (1,0)]), (0,0)) == deque([(0,0), (0,2)])
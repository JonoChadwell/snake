from search import *

def test_a_star_search():
    start = 1
    goal = 7

    assert a_star_search(
                start_state=start,
                heuristic=lambda x: abs(goal - x),
                list_adjacent=lambda x: [x + 1, x - 1]
            ) == [1,2,3,4,5,6,7]

    
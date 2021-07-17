from collections import deque

import common
import itertools
from search import a_star_search
from snake import Snake

# Algorithm idea:
# A "supercell" is a 2x2 area of the snake board

# Maintain a list of supercells that currently contain the snake, traversing this list by the right hand rule.
	
# When a new goal is revealed, make the adjustment to the list that most quickly reaches the goal tile. This adjustment can be made using A*.

# Only works on even * even grid sizes

def supercell(pos):
    """Return the position of the supercell containing a position."""
    return tuple([x - x % 2 for x in pos])

def subcell(pos):
    return tuple([x % 2 for x in pos])

SUPERCELL_DIRECTIONS = {
    (2,0),
    (-2,0),
    (0,2),
    (0,-2),
}

CLOCKWISE_IN_TABLE = {
    (0,0) : (1,0),
    (1,0) : (1,1),
    (1,1) : (0,1),
    (0,1) : (0,0)
}
def clockwise_in(pos):
    return common.add_elements(supercell(pos), CLOCKWISE_IN_TABLE[subcell(pos)])

CLOCKWISE_OUT_TABLE = {
    (0,0) : (0,-1),
    (1,0) : (2,0),
    (1,1) : (1,2),
    (0,1) : (-1,1)
}
def clockwise_out(pos):
    return common.add_elements(supercell(pos), CLOCKWISE_OUT_TABLE[subcell(pos)])

# Unused
def supercellerate(snake):
    """Convert from snake representation to supercell path representation.
    """
    current = (supercell(snake[0]), [])
    result = [current]
    for x in snake:
        if supercell(x) == current[0]:
            current[1].insert(0, x)
        else:
            current = (supercell(x), [x])
            result.append(current)

    return result

def clockwise_step(start, next):
    """Returns the next move to make given the current position and the
    supercell that we want to enter next.
    """
    in_next = clockwise_in(start)
    out_next = clockwise_out(start)
    return out_next if supercell(out_next) == next else in_next

def clockwise_rotate(value):
    return (-value[1], value[0])

def assert_path_valid(width, height, path, *, skip=True):
    """Checks that a path is valid. The default of |skip| may be adjusted to
    improve program runtime if safety checks are not desired.
    """
    if skip: return
    assert not (width % 2) and not (height % 2)
    assert isinstance(path, deque)
    for cell in path:
        assert supercell(cell) == cell
        assert common.in_bounds(cell, (width, height))
    if 1 < len(path):
        for idx in range(len(path)):
            assert common.subtract_elements(path[idx - 1], path[idx]) in SUPERCELL_DIRECTIONS

def clockwise_reachable(path, idx):
    """Given a path of supercells and an index into that path, return an
    iterable of cells that can be added to the path in with this element.
    """
    current = path[idx]
    if len(path) == 1:
        assert idx == 0
        return map(lambda x: common.add_elements(current, x), SUPERCELL_DIRECTIONS)

    before = path[idx - 1]
    after = path[(idx + 1) % len(path)]

    dir_before = common.subtract_elements(before, current)
    dir_after = common.subtract_elements(after, current)
    assert dir_before in SUPERCELL_DIRECTIONS
    assert dir_after in SUPERCELL_DIRECTIONS

    possible = []
    attempt = clockwise_rotate(dir_before)
    while attempt != dir_after:
        possible.append(attempt)
        attempt = clockwise_rotate(attempt)
    return map(lambda x: common.add_elements(current, x), possible)

def find_path_to_goal(width, height, old_path, goal, head_pos=None):
    assert not (width % 2) and not (height % 2)

    goal_cell = supercell(goal)

    # Supercells that contain the snake and thus cannot be entered normally.
    blocked = set()

    class Forward:
        def __init__(self, steps):
            self.steps = steps

    # TODO: reduce "blocked" to exclude cells that will be left before they
    # could possibly be reached.
    already_contained = False
    for cell in old_path:
        blocked.add(cell)
        if cell == goal_cell:
            already_contained = True
    assert not already_contained

    def list_adjacent(state):
        def test_position(x):
            return x not in blocked and common.in_bounds(x, (width, height))

        if isinstance(state, Forward):
            if state.steps + 1 < len(old_path):
                yield Forward(state.steps + 1)

            if state.steps == 0:
                if head_pos is None:
                    return
                pos = head_pos
                end = old_path[1 % len(old_path)]
                while (out_cell := common.add_elements(supercell(CLOCKWISE_OUT_TABLE[subcell(pos)]),
                            supercell(pos))) != end:
                    if test_position(out_cell):
                        yield out_cell
                    pos = common.add_elements(CLOCKWISE_IN_TABLE[subcell(pos)], supercell(pos))
                return

            yield from filter(test_position, clockwise_reachable(old_path, state.steps))
            return

        yield from filter(test_position, [
            common.add_elements(state, (2,0)),
            common.add_elements(state, (-2,0)),
            common.add_elements(state, (0,2)),
            common.add_elements(state, (0,-2)),
        ])
    
    def heuristic(state):
        if isinstance(state, Forward):
            return common.grid_distance(old_path[state.steps], goal) // 2
        return common.grid_distance(state, goal) // 2

    new_path = a_star_search(start_state=Forward(0), heuristic=heuristic, list_adjacent=list_adjacent)
    return list(map(lambda x: old_path[x.steps] if isinstance(x, Forward) else x, new_path))

def add_to_path(old_path, additions, idx):
    """Create a new path based on an old path with several cells added at a\
    given index.
    """

    sliceable = list(old_path)
    assert 0 <= idx and idx < len(old_path)
    assert sliceable[idx] == additions[0]
    assert additions[1] in clockwise_reachable(old_path, idx)

    new_path = deque()
    new_path.extend(sliceable[0:idx])
    new_path.extend(additions[:-1])
    new_path.extend(additions[::-1])
    new_path.extend(sliceable[idx+1:])

    return new_path

def update_path(width, height, old_path, goal, head_pos=None):
    assert_path_valid(width, height, old_path)
    path_to_goal = find_path_to_goal(width, height, old_path, goal, head_pos)

    idx = 0
    while idx < len(old_path) and old_path[idx] == path_to_goal[idx]:
        idx += 1
    assert idx > 0

    new_path = add_to_path(old_path, path_to_goal[idx - 1:], idx - 1)
    assert_path_valid(width, height, new_path)
    return new_path

def find_discardable(path, keep):
    """Returns an iterable of indicies that can be removed from a path without
    removing any tiles from |keep|.
    """
    stack = []
    for idx, location in enumerate(path):
        if len(stack) >= 2 and stack[-2][0] == location:
            yield stack.pop()[1]
            yield idx
            continue
        if location in keep:
            stack.clear()
        stack.append((location, idx))

def reduce_path(path, snake, goal):
    occupied = set()

    for location in snake:
        occupied.add(supercell(location))
    occupied.add(supercell(goal))

    drop = set()
    drop.update(find_discardable(path, occupied))

    if not drop:
        return path
    
    return deque(map(
        lambda x: x[1],
        filter(
            lambda x: x[0] not in drop,
            enumerate(path))))

def ai_supercellerator_v1(game):
    width = game.get_width()
    height = game.get_height()

    # Set AI data if it is missing
    occupying = game.get_ai_data()
    if occupying is None:
        assert len(game.get_snake_position()) <= 4
        position = supercell(game.get_snake_head())
        occupying = deque([
                position,
                common.add_elements(position, (2,0)),
                common.add_elements(position, (2,2)),
                common.add_elements(position, (2,0))])
        assert_path_valid(width, height, occupying)
        game.set_ai_data(occupying)

    goal = supercell(game.get_goal())
    if goal not in occupying:
        snake = game.get_snake_position()
        occupying = reduce_path(occupying, snake, goal)
        assert_path_valid(width, height, occupying)
        occupying = update_path(width, height, occupying, goal, snake[0])
        assert_path_valid(width, height, occupying)
        occupying = reduce_path(occupying, snake, goal)
        assert_path_valid(width, height, occupying)
        game.set_ai_data(occupying)

    head = game.get_snake_head()
    assert supercell(head) == occupying[0]
    next = clockwise_step(head, occupying[1])
    if supercell(next) == supercell(occupying[1]):
        occupying.append(occupying.popleft())

    return common.subtract_elements(next, head)

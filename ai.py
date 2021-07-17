from collections import deque
from collections import defaultdict

import common
import search
from snake import Snake
from bitset import Bitset

###############################################################################

def adjacent(width, height, position):
    """Get all in bound locations adjacent to position."""
    possible = [common.add_elements(position, x) for x in Snake.VALID_DIRECTIONS]
    return list(filter(
                lambda x: common.in_bounds(x, (width, height)),
                possible))

def shortest_path(width, height, start, end, blocked):
    """Find the shortest path from start to end on a width by height grid that
    doesn't pass through any squares in the "blocked" collection.
    """
    checked = set()
    blocked_set = set(blocked)
    blocked_set.discard(start)
    blocked_set.discard(end)

    def heuristic(position):
        return common.grid_distance(position, end)

    def list_moves(position):
        possible = list(filter(
                lambda x:  not x in checked
                    and not x in blocked_set,
                adjacent(width, height, position)))
        checked.update(possible)
        return list([common.subtract_elements(x, position) for x in possible])

    def apply_move(position, move):
        return common.add_elements(position, move)

    return search.original_a_star_search(
        start_state=start,
        heuristic=heuristic,
        list_moves=list_moves,
        apply_move=apply_move)

def flood_distance(width, height, target, snake):
    """Approximate the shortest possible path by which a snake can reach a
    target using a variant of flood fill.
    """
    assert common.in_bounds(target, (width, height))

    if snake[0] == target:
        return 0

    steps = 0
    fringe = defaultdict(list)
    fringe[0].append(snake[0])
    explored = {snake[0]}

    while True:
        front = fringe[steps]
        for search_from in front:
            possible_next_positions = adjacent(width, height, search_from)
            for next in possible_next_positions:
                if next in explored:
                    continue
                explored.add(next)

                next_steps = steps + 1
                if next in snake:
                    turns_till_available = len(snake) - snake.index(next) - 1
                    next_steps = max(next_steps, turns_till_available)

                if next == target:
                    return next_steps

                fringe[next_steps].append(next)
        steps = steps + 1
        if steps > len(snake) + width + height:
            raise Exception("Could not reach")


def supergrid_factor(width, height, snake):
    """Calculate the size of the largest area of connected 2x2 regions of the
    map."""

    # Build a set for fast access
    snake_set = set(snake)

    # Calculate supercell size
    def supercell_valid(x, y):
        return 0 <= x and x+1 < width \
            and 0 <= y and y+1 < height \
            and (x,y) not in snake_set \
            and (x+1,y) not in snake_set \
            and (x,y+1) not in snake_set \
            and (x+1,y+1) not in snake_set

    explored = set()
    largest_found = 0
    for x in range(0, width, 2):
        for y in range(0, height, 2):
            if not supercell_valid(x,y):
                continue
            if (x,y) in explored:
                continue
            
            # DFS for the connected components
            component = set()
            fringe = [(x,y)]
            while fringe:
                val = fringe.pop()
                if val not in component and supercell_valid(val[0], val[1]):
                    component.add(val)
                    fringe.append((val[0] + 2, val[1]))
                    fringe.append((val[0] - 2, val[1]))
                    fringe.append((val[0], val[1] + 2))
                    fringe.append((val[0], val[1] - 2))

            largest_found = max(largest_found, len(component))
            explored.update(component)
    
    return largest_found

def navigation_factor(width, height, snake):
    """Approximate difficulty of navigating the map by calculating a lower
    bound on the steps it would take to reach each other tile.
    """
    steps = 0
    fringe = defaultdict(list)
    fringe[0].append(snake[0])
    explored = {snake[0]}
    result = 0

    while len(explored) < width * height:
        front = fringe[steps]
        for search_from in front:
            possible_next_positions = adjacent(width, height, search_from)
            for next in possible_next_positions:
                if next in explored:
                    continue

                next_steps = steps + 1
                if next in snake:
                    turns_till_available = len(snake) - snake.index(next) - 1
                    next_steps = max(next_steps, turns_till_available)

                fringe[next_steps].append(next)
                explored.add(next)
                result += next_steps

        steps = steps + 1
        if steps > len(snake) + width + height:
            raise Exception("Could not reach all tiles")

    n = len(snake) - 1
    return result - (n * n + n) // 2

###############################################################################

def ai_run_right(x):
    return (1, 0)

def ai_towards_goal(game):
    goal = game.get_goal()
    pos = game.get_snake_head()
    
    if goal[0] < pos[0]:
        return Snake.WEST
    if goal[0] > pos[0]:
        return Snake.EAST
    if goal[1] < pos[1]:
        return Snake.NORTH
    if goal[1] > pos[1]:
        return Snake.SOUTH
    
    raise Exception("Goal at same place as head?")

def ai_smarter_towards_goal(game):
    idea = ai_towards_goal(game)
    snake = game.get_snake_position()

    if game.is_direction_safe(idea):
        return idea

    for backup in Snake.VALID_DIRECTIONS:
        if game.is_direction_safe(backup):
            return backup

    return Snake.NORTH

def ai_hamiltonian(game):
    width = game.get_width()
    height = game.get_height()
    x = game.get_snake_head()[0]
    y = game.get_snake_head()[1]

    if height % 2 != 0:
        raise Exception("Invalid height for hamiltonian snake")
    
    if x == 0 and y == 0:
        return Snake.SOUTH
    
    if y == 0:
        return Snake.WEST
    
    if x == width - 1:
        return Snake.NORTH

    if y == height - 1:
        return Snake.EAST

    if y % 2:
        if x == width - 2:
            return Snake.SOUTH
        return Snake.EAST

    if x == 0:
        return Snake.SOUTH
    return Snake.WEST

# Very Very Slow
def ai_bfs_goal(game):
    start_state = game.copy()
    start_state.first_move = None
    fringe = deque([start_state])

    while fringe:
        state = fringe.popleft()
        for dir in Snake.VALID_DIRECTIONS:
            new_state = state.copy()
            new_state.advance(dir)

            # Pass through the original move to get to this path.
            if state.first_move is None:
                new_state.first_move = dir
            else:
                new_state.first_move = state.first_move

            if new_state.get_state() == Snake.PLAYING:
                fringe.append(new_state)

            if new_state.get_points() > game.get_points():
                return new_state.first_move
    
    return Snake.NORTH

def ai_a_star_goal(game):
    goal = game.get_goal()

    def heuristic(game):
        head = game.get_snake_head()
        return common.grid_distance(head, goal)

    def list_moves(game):
        return list(filter(
                lambda x: game.is_direction_safe(x),
                Snake.VALID_DIRECTIONS))

    def apply_move(game, move):
        copy = game.copy()
        copy.advance(move)
        return copy

    path = search.original_a_star_search(
        start_state=game,
        heuristic=heuristic,
        list_moves=list_moves,
        apply_move=apply_move,
        copy_interval=0)

    if path:
        return path[0]
    return Snake.NORTH


def ai_a_star_culled(game):
    """As ai_a_star_goal but only consider options that lead the same set of
    filled squares once
    """
    goal = game.get_goal()
    tested = set()

    def to_bitset(game):
        res = Bitset()
        for x in range(game.get_width()):
            for y in range(game.get_height()):
                if (x,y) in game.get_snake_position():
                    res.set(x + y * game.get_width())
        return res

    def heuristic(game):
        head = game.get_snake_head()
        return common.grid_distance(head, goal)

    def list_moves(game):
        return list(filter(
                lambda x: game.is_direction_safe(x),
                Snake.VALID_DIRECTIONS))

    def apply_move(game, move):
        copy = game.copy()
        copy.advance(move)
        image = to_bitset(copy)
        if image in tested:
            return None
        tested.add(image)
        return copy

    path = search.original_a_star_search(
        start_state=game,
        heuristic=heuristic,
        list_moves=list_moves,
        apply_move=apply_move,
        copy_interval=0)

    if path:
        return path[0]
    return Snake.NORTH

def ai_a_star_culled_then_to_tail(game):
    """As ai_a_star_goal but only consider options that lead the same set of
    filled squares once
    """
    ai_data = game.get_ai_data()
    if ai_data:
        return ai_data.pop()

    goal = game.get_goal()
    tested = set()

    def to_dedupe(game):
        res = Bitset()
        for x in range(game.get_width()):
            for y in range(game.get_height()):
                if (x,y) in game.get_snake_position():
                    res.set(x + y * game.get_width())
        return (game.get_snake_head(), res)

    def heuristic(game):
        head = game.get_snake_head()
        return common.grid_distance(head, goal)

    def list_moves(game):
        return list(filter(
                lambda x: game.is_direction_safe(x),
                Snake.VALID_DIRECTIONS))

    def apply_move(game, move):
        copy = game.copy()
        copy.advance(move)

        dedupe = to_dedupe(copy)
        if dedupe in tested:
            return None
        tested.add(dedupe)

        # If a move would take you to the goal, make sure that after reaching
        # the goal you can then reach your own tail.
        if heuristic(copy) == 0:
            if shortest_path(
                        copy.get_width(),
                        copy.get_height(),
                        copy.get_snake_head(),
                        copy.get_snake_tail(),
                        copy.get_snake_position()
                    ) is None:
                return None

        return copy

    path = search.original_a_star_search(
        start_state=game,
        heuristic=heuristic,
        list_moves=list_moves,
        apply_move=apply_move,
        copy_interval=0)

    if path:
        game.set_ai_data(path[1:][::-1])
        return path[0]
    return Snake.NORTH

def ai_a_star_culled_always_tail(game):
    ai_data = game.get_ai_data()
    if ai_data:
        return ai_data.pop()

    goal = game.get_goal()
    tested = set()

    def to_dedupe(game):
        res = Bitset()
        for x in range(game.get_width()):
            for y in range(game.get_height()):
                if (x,y) in game.get_snake_position():
                    res.set(x + y * game.get_width())
        return (game.get_snake_head(), res)

    def heuristic(game):
        head = game.get_snake_head()
        return common.grid_distance(head, goal)

    def list_moves(game):
        return list(filter(
                lambda x: game.is_direction_safe(x),
                Snake.VALID_DIRECTIONS))

    def apply_move(game, move):
        copy = game.copy()
        copy.advance(move)
        
        # Make sure that you can reach your own tail from this position.
        if shortest_path(
                    copy.get_width(),
                    copy.get_height(),
                    copy.get_snake_head(),
                    copy.get_snake_tail(),
                    copy.get_snake_position()
                ) is None:
            return None

        dedupe = to_dedupe(copy)
        if dedupe in tested:
            return None
        tested.add(dedupe)

        return copy

    path = search.original_a_star_search(
        start_state=game,
        heuristic=heuristic,
        list_moves=list_moves,
        apply_move=apply_move,
        copy_interval=0)

    if path:
        game.set_ai_data(path[1:][::-1])
        return path[0]
    return Snake.NORTH

def ai_a_star_culled_always_tail_better_heuristic(game):
    ai_data = game.get_ai_data()
    if ai_data:
        return ai_data.pop()

    goal = game.get_goal()
    tested = set()

    def to_dedupe(game):
        res = Bitset()
        for x in range(game.get_width()):
            for y in range(game.get_height()):
                if (x,y) in game.get_snake_position():
                    res.set(x + y * game.get_width())
        return (game.get_snake_head(), res)

    def heuristic(game):
        head = game.get_snake_head()
        return flood_distance(game.get_width(), game.get_height(), goal,
                game.get_snake_position())

    def list_moves(game):
        return list(filter(
                lambda x: game.is_direction_safe(x),
                Snake.VALID_DIRECTIONS))

    def apply_move(game, move):
        copy = game.copy()
        copy.advance(move)
        
        # Make sure that you can reach your own tail from this position.
        if shortest_path(
                    copy.get_width(),
                    copy.get_height(),
                    copy.get_snake_head(),
                    copy.get_snake_tail(),
                    copy.get_snake_position()
                ) is None:
            return None

        dedupe = to_dedupe(copy)
        if dedupe in tested:
            return None
        tested.add(dedupe)

        return copy

    path = search.original_a_star_search(
        start_state=game,
        heuristic=heuristic,
        list_moves=list_moves,
        apply_move=apply_move,
        copy_interval=0)

    if path:
        game.set_ai_data(path[1:][::-1])
        return path[0]
    return Snake.NORTH

def ai_a_star_limited(game):
    SEARCH_LIMIT = 1000
    ai_data = game.get_ai_data()
    if ai_data:
        return ai_data.pop()

    goal = game.get_goal()

    def heuristic(game):
        head = game.get_snake_head()
        return common.grid_distance(head, goal)

    def list_moves(game):
        return list(filter(
                lambda x: game.is_direction_safe(x),
                Snake.VALID_DIRECTIONS))

    def apply_move(game, move):
        copy = game.copy()
        copy.advance(move)
        
        # Make sure that you can reach your own tail from this position.
        if shortest_path(
                    copy.get_width(),
                    copy.get_height(),
                    copy.get_snake_head(),
                    copy.get_snake_tail(),
                    copy.get_snake_position()
                ) is None:
            return None
        return copy

    path = search.original_a_star_search(
        start_state=game,
        heuristic=heuristic,
        list_moves=list_moves,
        apply_move=apply_move,
        copy_interval=0,
        search_limit=SEARCH_LIMIT)

    if path:
        game.set_ai_data(path[1:][::-1])
        return path[0]

    head = game.get_snake_head()
    tail = game.get_snake_tail()
    blocked = list(filter(lambda x: x != head and x != tail, game.get_snake_position()))
    path = shortest_path(
        width=game.get_width(),
        height=game.get_height(),
        start=head,
        end=tail,
        blocked=blocked)

    if path:
        game.set_ai_data(path[1:][::-1])
        return path[0]
    
    return Snake.NORTH

def ai_simple_explore(game):
    MAX_DEPTH = 5

    goal = game.get_goal()
    starting_points = game.get_points()

    def heuristic(game):
        base = game.get_width() + game.get_height()
        if game.get_points() > starting_points:
            return base + game.get_moves_since_point()
        return base - common.grid_distance(game.get_snake_head(), goal)

    def list_moves(game):
        return list(filter(
                lambda x: game.is_direction_safe(x),
                Snake.VALID_DIRECTIONS))

    def apply_move(game, move):
        copy = game.copy()
        copy.advance(move)
        
        # Make sure that you can reach your own tail from this position.
        if shortest_path(
                    copy.get_width(),
                    copy.get_height(),
                    copy.get_snake_head(),
                    copy.get_snake_tail(),
                    copy.get_snake_position()
                ) is None:
            return None
        return copy

    path = search.explore_state_space(
        start_state=game,
        heuristic=heuristic,
        list_moves=list_moves,
        apply_move=apply_move,
        depth=MAX_DEPTH)

    if path:
        return path[0]

    return Snake.NORTH

def ai_complex_explore(game):
    DEPTH = 4

    goal = game.get_goal()
    starting_points = game.get_points()

    starting_nav=navigation_factor(game.get_width(), game.get_height(), game.get_snake_position())

    def heuristic(game):
        def want_points():
            if game.get_points() > starting_points:
                return common.sigmoid(game.get_moves_since_point())
            else:
                return common.sigmoid(-flood_distance(
                    game.get_width(),
                    game.get_height(),
                    goal,
                    game.get_snake_position()))

        def want_supergrid():
            w = game.get_width()
            h = game.get_height()
            snake = game.get_snake_position()
            return supergrid_factor(w, h, snake) / ((w // 2) * (h // 2) - len(snake) / 4 + 1)

        def want_navigability():
            nav = navigation_factor(game.get_width(), game.get_height(), game.get_snake_position())
            return common.sigmoid(starting_nav - nav)

        p = want_points()
        s = want_supergrid()
        n = want_navigability()
        return p * (2 + game.get_moves_since_point() / 5) \
                + s \
                + n

    def list_moves(game):
        return list(filter(
                lambda x: game.is_direction_safe(x),
                Snake.VALID_DIRECTIONS))

    def apply_move(game, move):
        copy = game.copy()
        copy.advance(move)
        
        # Make sure that you can reach your own tail from this position.
        if shortest_path(
                    copy.get_width(),
                    copy.get_height(),
                    copy.get_snake_head(),
                    copy.get_snake_tail(),
                    copy.get_snake_position()
                ) is None:
            return None
        return copy

    path = search.explore_state_space(
        start_state=game,
        heuristic=heuristic,
        list_moves=list_moves,
        apply_move=apply_move,
        depth=DEPTH)

    if path:
        return path[0]

    return Snake.NORTH

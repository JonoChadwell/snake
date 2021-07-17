from queue import PriorityQueue
from collections import deque

def original_a_star_search(*, start_state, heuristic, list_moves, apply_move,
        copy_interval=-1, search_limit=0):
    """Perform an A* search through a state space.
    
    Assumes that the cost of each move is one.

    Returns 'None' if no path is found.

    Required keyword arguments:
    start_state -- The starting point
    heuristic -- Given a state return an "admissible" guess for its proximity
        to the goal state. Should return '0' if the state is in the goal state.
    list_moves -- Given a state return a list of legal "moves" to make from
        that state.
    apply_move -- Given a state and a move, create a new state with that move
        applied. May return None to indicate that a move is not possible.

    Optional keyword arugments:
    copy_interval -- By default (-1) the game state will be reconstructed from
        the base state each time. Setting to "0" will make a copy for every 
        state explored. A larger value will cache a state every <x> layers.
        This has no impact on output and is purely a performance optimiziation.
    search_limit -- If provided, search no more than this number of state before
        returning None.
    """

    fringe = PriorityQueue()
    # Fringe contents are a tuple with:
    # (ranking, counter, move_list, num_applied_moves, base_state)
    counter = 0
    fringe.put((0, counter, [], 0, start_state))

    while not fringe.empty():
        counter = counter + 1
        if search_limit > 0 and counter > search_limit:
            return None

        node = fringe.get()
        current_path = node[2]
        num_applied_moves = node[3]
        state = node[4]

        # Re-construct the current state
        for move in current_path[num_applied_moves::]:
            if state is not None:
                state = apply_move(state, move)
        if state is None:
            continue
        
        possible_moves = list_moves(state)

        for move in possible_moves:
            cost = len(current_path) + 1
            new_path = current_path + [move]
            new_state = apply_move(state, move)
            if new_state is None:
                continue
            heuristic_value = heuristic(new_state)

            if heuristic_value == 0:
                return new_path
            
            if copy_interval >= 0 and cost - num_applied_moves > copy_interval:
                fringe.put((cost + heuristic_value, counter, new_path, len(new_path), new_state))
            else:
                fringe.put((cost + heuristic_value, counter, new_path, num_applied_moves, node[4]))
    
    return None

def a_star_search(*, start_state, heuristic, list_adjacent):
    """Perform an A* search through a state space.
    
    Assumes that the cost of each state transition is one.

    Returns a list of states that reaches the goal state, or 'None' if no path
    is found.

    Required keyword arguments:
    start_state -- The starting point
    heuristic -- Given a state return an "admissible" guess for its proximity
        to the goal state. Should return '0' if the state is in the goal state.
    list_adjacent -- Given a state return an iterable of states that can be
        reached from that state.
    """

    def collapse_path(x):
        res = []
        while x:
            res.append(x[0])
            x = x[1]
        return res[::-1]

    explored = set([start_state])
    fringe = PriorityQueue()
    # Fringe contents are a tuple with:
    # (ranking, counter, cost, state)
    counter = 0
    fringe.put((0, counter, start_state, 0, (start_state, False)))


    while not fringe.empty():
        node = fringe.get()
        state = node[2]
        cost = node[3]
        path = node[4]

        for new_state in list_adjacent(state):
            counter = counter + 1
            if new_state in explored:
                continue
            explored.add(new_state)

            heuristic_value = heuristic(new_state)
            new_cost = cost + 1
            new_path = (new_state, path)

            if heuristic_value == 0:
                return collapse_path(new_path)
            
            fringe.put((cost + heuristic_value, counter, new_state, new_cost, new_path))
    
    return None

def explore_state_space(*, start_state, list_moves, apply_move, heuristic,
        depth=3):
    """Perform a search through a state space, looking for a "best" path.
    
    Required keyword arguments:
    start_state -- The starting state.
    list_moves -- Given a state return a list of possible moves.
    apply_move -- Create a new state given a move and a previous state. May
        return None if that state is not worth evaluating further.
    heuristic -- Calculate the score of a state. The state with the highest
        evaluated score will be returned.

    Optional keyword arugments:
    depth -- The depth at which to evaluate the heuristics.
    """

    fringe = [(start_state, [])]
    to_check = []

    while fringe:
        state, path = fringe.pop()
        moves = list_moves(state)
        for move in moves:
            new_state = apply_move(state, move)
            new_path = path + [move]
            if new_state is None:
                continue
            if len(new_path) >= depth:
                to_check.append((new_state, new_path))
            else:
                fringe.append((new_state, new_path))
    
    best_score = 0
    best_path = None
    for state, path in to_check:
        score = heuristic(state)
        if best_score < score:
            best_score = score
            best_path = path
    
    return best_path

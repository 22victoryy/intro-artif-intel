#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

# import os #for time functions

from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS #for Sokoban specific classes and problems

#NOTE - tested at CDF, results match the output of local machine
#
def sokoban_goal_state(state):
  '''
  @return: Whether all boxes are stored.
  '''
  for box in state.boxes:
    if box not in state.storage:
      return False
  return True

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid. --> no obstacles
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.

    # access all the storages in the boxes
    # manhattan distance = (x1-x2) + (y2-y1) coords

    man_heur = 0
    for box in state.boxes: # iterate through all the boxes
        man_distances = []  # empty list to store all the manhattan distances of the boxes
        for storage in state.storage: # iterate through the storages
            #  (x1-y1) + (x2-y2)
            man_distances.append(abs(box[0] - storage[0]) + abs(box[1] - storage[1]))
        # add shortest manhattan distance to total dist
        man_heur += min(man_distances)

    return man_heur

#SOKOBAN HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
  count = 0
  for box in state.boxes:
    if box not in state.storage:
        count += 1
  return count

def obstacles(start, dest, state):
    """
    :param start:
    :type start:
    :param dest:
    :type dest:
    :param state:
    :type state:
    :return:
    :rtype:
    """
    #return numbers of obstacles from start to dest
    #robots on the way also considered as obstacles
    total = 0
    robots = frozenset(state.robots)
    blockades = state.obstacles.union(robots)
    for obstacle in blockades:
        if max(dest[0], start[0]) > obstacle[0] > min(start[0], dest[0]):
            if max(dest[1], start[1]) > obstacle[1]> min(start[1], dest[1]):
                total += 1
    return total


def avail_storage(box, state):
    """
    :param box:
    :type box:
    :param state:
    :type state:
    :return:
    :rtype:
    """
    # add all the storages
    storages = []
    for storage in state.storage:
        storages.append(storage)

    # remove other boxes in the storage if there are occupied
    for other in state.boxes:
        if other in storages:
            if box != other:
                storages.remove(other)
    return storages

def check_deadlocked(position, state):
    """
    :param position:
    :type position:
    :param state:
    :type state:
    :return:
    :rtype:
    """
    # check if the box is deadlocked
    blockades = state.obstacles.union(state.boxes)

    #(x, y) --> box positions, (x, y)
    up = (position[0], position[1] + 1)
    down = (position[0], position[1] - 1)
    left = (position[0] - 1, position[1])
    right = (position[0] + 1, position[1])

    #if there are walls,then any consecutive boxes are immovable
    if position[0] == 0:
        if position[1] == 0:
            return True
        elif up in blockades:
            return True
        elif down in blockades:
            return True
        elif right in blockades:
            return True

    if position[0] == state.width - 1:
        if position[1] == state.height - 1:
            return True
        elif position[1] == 0:
            return True
        elif left in blockades:
            return True
        elif up in blockades:
            return True
        elif down in blockades:
            return True

    if position[1] == state.height - 1:
        if position[0] == state.width - 1:
            return True
        elif position[0] == 0:
            return True
        elif left in blockades:
            return True
        elif right in blockades:
            return True
        elif up in blockades:
            return True

    if position[1] == 0:
        if position[0] == 0:
            return True
        elif left in blockades:
            return True
        elif right in blockades:
            return True
        elif down in blockades:
            return True


def heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current
    # state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.

    # box to goal distance + robot to the box distance = altn_heur
    for box in state.boxes:
        avail_storages = avail_storage(box, state)
        if box not in avail_storages:
            if check_deadlocked(box, state):
                return float("inf")
    else:
        # add the distances from the box to the goal
        altn_heur = 0
        for box in state.boxes:
            box_cost = float("inf")
            available = avail_storage(box, state)
            for storages in available:
                current_cost = abs(box[0] - storages[0]) + abs(box[1] - storages[1]) + \
                               obstacles(box, storages, state) * 2

                if current_cost < box_cost:
                    box_cost = current_cost

            altn_heur += box_cost


        for robot in state.robots:
            # find the distance of the closest storage for each robot
            closest = float("inf")
            for box in state.boxes:
                if (abs(box[0] - robot[0]) + abs(box[1] - robot[1]) + obstacles(robot, box, state) * 2) < closest:
                    closest = abs(box[0] - robot[0]) + abs(box[1] - robot[1]) + obstacles(robot, box, state) * 2
            altn_heur += closest

        return altn_heur

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.

    return (weight * sN.hval) + sN.gval


def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound=10):
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''

    state_inf = float('inf')

    # initialise time_start
    time_start = os.times()[0]  # search start time_start
    end_time = time_start + timebound  # search end time_start

    weight_fval = (lambda sN: fval_function(sN, weight)) #wrapped

    # Initialize Searcher
    search_util = SearchEngine('custom', 'default')
    search_util.init_search(initial_state, sokoban_goal_state, heur_fn, weight_fval)

    bound_limit = timebound  # timebound

    cost_bound = (state_inf, state_inf, state_inf)  # None...?
    final = search_util.search(bound_limit)  # start searching with the time bound

    # cost_bound = None
    soln = False

    while time_start < end_time:
        if final == False:  # base case, if soln not found
            return soln
        else:
            time_passed = os.times()[0] - time_start
            bound_limit -= time_passed

            # prune
            if final.gval <= cost_bound[0]:
                cost_bound = (final.gval - 1, final.gval -1 , final.gval -1)
                soln = final
            final = search_util.search(bound_limit, cost_bound)
    return soln


def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of anytime gbfs algorithm'''
  state_inf = float('inf')

  # initialise time_start
  time_start = os.times()[0] # search start time_start
  end_time = time_start + timebound  # search end time_start

  # Initialize Searcher
  search_util = SearchEngine('best_first', 'default')
  search_util.init_search(initial_state, sokoban_goal_state, heur_fn)


  bound_limit = timebound  #timebound

  cost_bound = (state_inf, state_inf, state_inf) # None...?
  final = search_util.search(bound_limit) # start searching with the time bound

  # cost_bound = None
  soln = False

  while time_start < end_time:
    if final == False: # base case, if soln not found
        return soln
    else:
        time_passed = os.times()[0] - time_start
        bound_limit -= time_passed

        # prune
        if final.gval <= cost_bound[0]:
            cost_bound = (final.gval, final.gval, final.gval)
            soln = final
        final = search_util.search(bound_limit, cost_bound)
  return soln



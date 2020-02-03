#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

# import os #for time functions

from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS #for Sokoban specific classes and problems
# from itertools import product

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

def ob(start, dest, state):
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
    num = 0
    obs = state.obstacles.union(state.robots)

    max_distx = max(dest[0], start[0])
    min_distx = min(dest[0], start[0])
    max_disty = max(dest[1], start[1])
    min_disty = min(dest[1], start[1])

    for obstacle in obs:
        if max_distx > obstacle[0] > min_distx and max_disty> obstacle[1]> min_disty:
                num += 1
    return num

def fetch_storage(state):
    """
    gets the storage.
    """
    storages = []
    # convert frozenset to list to make it indexable
    storage_list = list(state.storage)

    i = 0
    while i < len(storage_list):
        strg = storage_list[i]
        storages.append(strg)
        i += 1
    return storages

def rm(box, state):
    """
    Empty the storage from other boxes that are occupying them...
    """
    storages = fetch_storage(state)
    box_list = list(state.boxes)

    for i in box_list:
        if i not in storages:
            continue
        else:
            if i != box:
                storages.remove(i)
    return storages

def ch_dlock(position, state):
    """
    Check deadlocks
    """
    # check if the box is deadlocked
    ob = state.obstacles.union(state.boxes)

    #(x, y) --> box positions, (x, y)
    up = (position[0], position[1] + 1)
    down = (position[0], position[1] - 1)
    left = (position[0] - 1, position[1])
    right = (position[0] + 1, position[1])

    if position[0] == 0 and position[1] == 0:
        return True
    elif position[0] == 0 and up in ob:
        return True
    elif position[0] == 0 and down in ob:
        return True
    elif position[0] == 0 and right in ob:
        return True

    elif position[1] == 0 and position[0] == 0:
        return True
    elif position[1] == 0 and left in ob:
        return True
    elif position[1] == 0 and right in ob:
        return True
    elif position[1] == 0 and down in ob:
        return True

    elif position[0] == state.width - 1 and position[1] == state.height - 1:
        return True
    elif position[0] == state.width - 1 and position[1] == 0:
        return True
    elif position[0] == state.width - 1 and left in ob:
        return True
    elif position[0] == state.width - 1 and up in ob:
        return True
    elif position[0] == state.width - 1 and down in ob:
        return True

    elif position[1] == state.height - 1 and position[0] == state.width - 1:
        return True
    elif position[1] == state.height - 1 and position[0] == 0:
        return True
    elif position[1] == state.height - 1 and left in ob:
        return True
    elif position[1] == state.height - 1 and right in ob:
        return True
    elif position[1] == state.height - 1 and up in ob:
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
    state_inf = float("inf")


    # iterate through all the boxes, if box free check deadlocked else exit loop
    # for all boxes, calculate the manhattan distance from box to storage, and add the number of obstacles it needs to
    # bypass....
    # for robots, calculate the manhattan distance of robot and box, adding the number of obstacles it needs to bypass

    # add all those up to get the final numeral heuristic value

    # decrease complexity
    for box in state.boxes:
        avail_storages = rm(box, state)
        if box in avail_storages:
            continue
        else:
            if ch_dlock(box, state):
                return state_inf
    else:
        altn_heur = 0
        for box in state.boxes:
            box_cost = state_inf

            available = rm(box, state)
            for storages in available:
                curr_cost = abs(box[0] - storages[0]) + abs(box[1] - storages[1]) + \
                            ob(box, storages, state) * 2

                if curr_cost < box_cost:
                    box_cost = curr_cost
            altn_heur += box_cost

        for robot in state.robots:
            if len(state.robots) < 10:
                nearest_distance = state_inf
                for box in state.boxes:
                    if (abs(box[0] - robot[0]) + abs(box[1] - robot[1]) + ob(robot, box, state) * 2) < nearest_distance:
                        nearest_distance = abs(box[0] - robot[0]) + abs(box[1] - robot[1]) + ob(robot, box, state) * 2
                altn_heur += nearest_distance

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

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound=10):  #pruning
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    state_inf = float('inf')

    weight_fval = (lambda sN: fval_function(sN, weight)) # weight
    search_util = SearchEngine('custom', 'default')
    search_util.init_search(initial_state, sokoban_goal_state, heur_fn, weight_fval)

    # start the timer
    time_start = os.times()[0]  # usertime
    end_time = time_start + timebound  # search end time_start

    final = search_util.search(timebound)  # start searching with the time bound

    soln = False
    while time_start < end_time:
        if final is not False:
            cost_bound = (state_inf, state_inf, state_inf)
            time_passed = os.times()[0] - time_start
            timebound -= time_passed

            # prune...
            if final.gval  <= cost_bound[0]:
                # weight -= 1 # prune on the weight
                cost_bound = (final.gval, final.gval, final.gval)
                soln = final
            final = search_util.search(timebound, cost_bound)
        else:
            return soln
    return soln


def anytime_gbfs(initial_state, heur_fn, timebound = 10):  #pruning? on gval?
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of anytime gbfs algorithm'''

  state_inf = float('inf')

  search_util = SearchEngine('best_first', 'default')
  search_util.init_search(initial_state, sokoban_goal_state, heur_fn)

  time_start = os.times()[0] # user time
  end_time = time_start + timebound  # search end time_start

  # instantiate search

  final = search_util.search(timebound) # start searching with the time bound

  soln = False
  while time_start < end_time:
    if final is not False:
        cost_bound = (state_inf, state_inf, state_inf)
        time_passed = os.times()[0] - time_start

        timebound -= time_passed

        gvalue = final.gval
        if gvalue < cost_bound[0]:
            gvalue -= 1 #prune on the gvalue
            cost_bound = (final.gval, final.gval, final.gval)
            soln = final
        final = search_util.search(timebound, cost_bound) # time passed
    else:
        return soln
  return soln


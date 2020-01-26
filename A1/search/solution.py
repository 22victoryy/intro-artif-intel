#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os #for time functions
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS #for Sokoban specific classes and problems

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

    # Pseudocode

    # access all the storages in the boxes
    # manhattan distance = (x1-x2) + (y2-y1) coords

    total_dist = 0
    for box in state.boxes: # iterate through all the boxes
        man_distances = []  # empty list to store all the manhattan distances of the boxes
        for storage in state.storage: # iterate through the storages
            #  (x1-x2) + (y1-y2)
            man_distances.append(abs(box[0] - storage[0]) + abs(box[1] - storage[1]))
        # add shortest manhattan distance to total dist
        total_dist += min(man_distances)

    return total_dist

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


def heur_alternate(state):
    #IMPLEMENT
    '''a better sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    return False
    # result = 0
    # robot_box_dists = []  # distance from robot to each box
    # for box in state.boxes:
    #     distances = []
    #     # calculate distance from robot to this box
    #     # print((state.robots[0])[1])
    #     # print(box[0])
    #     # print((state.robots[1])[1])
    #     # print(box[1])
    #     # a = (state.robots[0])[1]
    #     # b = (state.robots[1])[1]
    #
    #     # print(box[1])
    #
    #     # robot_box_dists.append(abs(state.robots[0] - box[0]) + abs(state.robots[1] - box[1]))
    #     # check if this state is deadlocked
    #     if trapped(box[0], box[1], state.height, state.width, state.obstacles, state.storage):
    #         result += 2
    #     for goal in state.storage:
    #         # if state.restrictions is None or goal in state.restrictions[state.boxes[box]]:
    #         distances.append(abs(box[0] - goal[0]) + abs(box[1] - goal[1]))
    #     if distances:
    #         result += min(distances)
    #
    # # result += min(robot_box_dists)
    # return result




























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

    # f value = cost + heuristic
    return (weight * sN.hval) + sN.gval












def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  # start_time = os.times()[0]
  # we are adding the weight to the astar search, therefore this will be custom
  # search all the spaces
  # search_util = SearchEngine('custom', 'full')
  # wrapped_fval_function = (lambda sN: fval_function(sN, weight))
  # search_util.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_function)
  #
  # goal = search_util.search(timebound)
  # if goal:
  #
  #     costbound = goal.gval + heur_fn(goal)  # Costbound.
  #     time_remaining = timebound - (os.times()[0] - start_time)
  #     best = goal
  #     while time_remaining > 0:  # While there is still time.
  #         initial_time = os.times()[0]
  #         new_goal = search_util.search(time_remaining, costbound=(float("inf"), float("inf"), costbound))
  #         time_remaining = time_remaining - (os.times()[0] - initial_time)  # Update remaining time.
  #
  #         if new_goal:
  #             costbound = new_goal.gval + heur_fn(new_goal)
  #             best = new_goal
  #     return best  # Return the best state.
  # else:
  #   return False




def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of anytime gbfs algorithm'''

  # time = os.times()[0] # start time
  # end_time = time + timebound  #end time
  # new_timebound = timebound  #timebound
  #
  # # Initialize Searcher
  # searcher = SearchEngine('best_first', 'default')
  # searcher.init_search(initial_state, sokoban_goal_state, heur_fn)
  #
  # # Perform  search and gather time
  # cost_bound = (float("inf"), float("inf"), float("inf"))
  # # cost_bound = None
  # best_result = False
  # result = searcher.search(new_timebound)  #costbound
  #
  # # Perform the search while the timebound has not been reached
  # while time < end_time:
  #   if result == False:
  #       # If no result found
  #       return best_result
  #   diff_time = os.times()[0] - time
  #   time = os.times()[0]        # Get current time
  #   new_timebound -= diff_time
  #   if result.gval <= cost_bound[0]:
  #       cost_bound = (result.gval, result.gval, result.gval)
  #       best_result = result
  #   result = searcher.search(new_timebound, cost_bound)
  # return best_result








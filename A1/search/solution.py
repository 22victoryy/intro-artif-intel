#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

# import os #for time functions

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

###################################################################

# box is deadlocked by obstacles
# deadlocked by walls
# if on the wall, not pushable
# if on the edge but storage is not in the way, then doomed
# if box in the corner, not possible
# closest two boxes?


def manhattan_distance(x, y):
    """
    :param x:
    :type x:
    :param y:
    :type y:
    :return:
    :rtype:
    """
    #return the manhattan distance between x and y
    return abs(x[0]-y[0])+abs(x[1]-y[1])

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
    cast_rob= frozenset(state.robots)
    all_obs= state.obstacles.union(cast_rob)
    for obst in all_obs:
        if max(dest[0], start[0]) > obst[0] > min(start[0], dest[0]):
            if max(dest[1], start[1])> obst[1]> min(start[1], dest[1]):
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
    # see the storage is avaliable,
    # remove from the list if the any storage is already occupied.
    possible = []
    for place in state.storage:
        possible.append(place)

    # remove other boxes in the storage if there are occupied
    for other_boxes in state.boxes:
        if box != other_boxes:
            if other_boxes in possible:
                possible.remove(other_boxes)
    return possible

def check_deadlocked(box_pos, state):
    """
    :param box_pos:
    :type box_pos:
    :param state:
    :type state:
    :return:
    :rtype:
    """
    # check if the box is deadlocked

    obst_list = state.obstacles | state.boxes

    #(x, y) --> box pos
    up_pos= (box_pos[0],box_pos[1]+1)
    down_pos= (box_pos[0],box_pos[1]-1)
    left_pos= (box_pos[0]-1,box_pos[1])
    right_pos= (box_pos[0]+1,box_pos[1])

    #if there are walls,then any consecutive boxes are immovable
    if box_pos[0] == 0:
        if box_pos[1] == 0:
            return True
        if box_pos[1] == state.height - 1:
            return True
        if up_pos in obst_list:
            return True
        if down_pos in obst_list:
            return True
        if left_pos in obst_list:
            return True
        if right_pos in obst_list:
            return True
        # if box_pos in obst_list:
        #     return True
        return False

    if box_pos[0] == state.width - 1:
        if box_pos[1] == 0:
            return True
        if  left_pos in obst_list:
            return True
        if right_pos in obst_list:
            return True
        if box_pos[1] == state.height - 1:
            return True
        if up_pos in obst_list:
            return True
        if down_pos in obst_list:
            return True
        return False

################# DO NOT TOUCH ABOVE THIS ####################
    if box_pos[1] == state.height - 1:
        if box_pos[0] == 0:
            return True
        # if up_pos or down_pos or left_pos or right_pos in obst_list:
        #     return True
        if left_pos in obst_list:
            return True
        if right_pos in obst_list:
            return True
        return False

    if box_pos[1] == 0:
        # if box_pos[0] in obst_list:
        #     return True
        if left_pos in obst_list:
            return True
        if right_pos in obst_list:
            return True
        # if up_pos in obst_list:
        #     return True
        # if down_pos in obst_list:
        #     return True
        return False

    #idk................?

    #no walls but surrounded by obstacles
    if up_pos in state.obstacles:
        if left_pos in state.obstacles:
            return True
        if right_pos in state.obstacles:
            return True
        return False
    if down_pos in state.obstacles:
        if left_pos in state.obstacles:
            return True
        if right_pos in state.obstacles:
            return True
        return False

    # if left_pos in state.obstacles:
    #     if up_pos in state.obstacles:
    #         return True
    #     if down_pos in state.obstacles:
    #         return True
    #     return False
    # if right_pos in state.obstacles:
    #     if up_pos in state.obstacles:
    #         return True
    #     if down_pos in state.obstacles:
    #         return True
    #     return False


    # possible_storage_pos = avail_storage(box_pos, state)
    #
    #
    # x_list = [pos[0] for pos in possible_storage_pos]
    # y_list = [pos[1] for pos in possible_storage_pos]

    # if box_pos[0] == 0:
    #     if not any(i == 0 for i in x_list):
    #         return True
    # if box_pos[0] == (state.width - 1):
    #     if not any(i == (state.width - 1) for i in x_list):
    #         return True
    # if box_pos[1] == (state.height - 1):
    #     if not any(i == state.height - 1 for i in y_list):
    #         return True
    # if box_pos[1] == 0:
    #     if not any(i == 0 for i in y_list):
    #         return True

    return False

def heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current
    # state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.

    alternate = 0
    # our cost consist of two components:
    #  the cost of the box in current position to our final storage +
    #  the cost of (closest) robert need to walk to position of the box
    for box in state.boxes:
        avail_storages = avail_storage(box, state)
        if box not in avail_storages:
            if check_deadlocked(box, state):
                return float("inf")
    else:
        #add the distances from the box to the goal
        cost = 0
        # for box in state.boxes:
        for box in state.boxes:
            possible_positions = avail_storage(box, state)
            cost_each_box = float("inf")
            for possibility in possible_positions:
                # manhattan_distance(possibility, box)
                current_cost = manhattan_distance(box, possibility) + obstacles(box, possibility, state) * 2
                # current_cost = (manhattan_distance(possibility, box) + obstacles(box, possibility, state)) * 2
                if current_cost < cost_each_box:
                    cost_each_box = current_cost
            cost += cost_each_box


        for rob in state.robots:
            # find the distance of the closest storage for each robot
            closest = float("inf")
            for box in state.boxes:
                if (manhattan_distance(box, rob) + obstacles(rob, box, state) * 2) < closest:
                # if (abs(box[0] + rob[0]) + obstacles(rob, box, state) * 2) < closest:
                    closest = manhattan_distance(box, rob) + obstacles(rob, box, state) * 2
            cost += closest
         # add the distances from the robot to the box
        alternate += cost
        return alternate # return the alternate heuristic numeric value

#######################################################################################

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


def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound=10):
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''

    state_inf = float("inf")

    # Initialize time
    time = os.times()[0]
    end_time = time + timebound
    bound_limit = timebound

    # Initialize fval with weight adjusted...not sure
    weight_fval = (lambda sN: fval_function(sN, weight)) #wrapped

    # initialise search engine
    search_util = SearchEngine('custom', 'default')
    search_util.init_search(initial_state, sokoban_goal_state, heur_fn, weight_fval)

    # Initialize cost bounds and variables
    cost = (state_inf, state_inf, state_inf) #None..?

    # final state
    final = search_util.search(timebound)

    not_found = False
    # Perform search while within the timebound
    while time < end_time:
        if final == False:  # base case, final not found
            return not_found
        else:
            # subtract the time cost from the restricted timebound
            diff_time = os.times()[0] - time
            # time = os.times()[0]
            bound_limit -= diff_time

            # if the cost of state is less than the current costbound...
            if final.gval <= cost[0]:
                cost = (final.gval, final.gval, final.gval)
                not_found = final
            final = search_util.search(bound_limit, cost)
    return not_found


def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of anytime gbfs algorithm'''

  state_inf = float('inf')

  # Initialize Searcher
  search_util = SearchEngine('best_first', 'default')
  search_util.init_search(initial_state, sokoban_goal_state, heur_fn)


  # initialise time_start
  time_start = os.times()[0] # search start time_start
  end_time = time_start + timebound  # search end time_start

  bound_limit = timebound  #timebound

  final = search_util.search(bound_limit) # start searching with the timebound

  cost_bound = (state_inf, state_inf, state_inf) # should I just reassign as None

  # If search did not find a goalstate
    # return False
  # Otherwse, keep going

  # cost_bound = None
  not_found = False


  # Perform the search while the timebound has not been reached
  while time_start < end_time:
    if final == False: # base case, if final not found
        return not_found
    else:
        time_passed = os.times()[0] - time_start

        time_start = os.times()[0]

        bound_limit -= time_passed

        if final.gval <= cost_bound[0]:
            cost_bound = (final.gval, final.gval, final.gval)
            not_found = final
        final = search_util.search(bound_limit, cost_bound)
  return not_found



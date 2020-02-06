#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

# import os #for time functions

from search import *  # for search engines
from sokoban import SokobanState, Direction, PROBLEMS  # for Sokoban specific classes and problems


# from itertools import product

# NOTE - tested at CDF, results match the output of local machine
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
    # IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # We want an admissible heuristic, which is an optimistic heuristic.
    # It must never overestimate the cost to get from the current state to the goal.
    # The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    # When calculating distances, assume there are no obstacles on the grid. --> no obstacles
    # You should implement this heuristic function exactly, even if it is tempting to improve it.
    # Your function should return a numeric value; this is the estimate of the distance to the goal.

    # access all the storages in the boxes
    # manhattan distance = (x1-x2) + (y2-y1) coords
    man_heur = 0
    for box in state.boxes:  # iterate through all the boxes
        man_distances = []  # empty list to store all the manhattan distances of the boxes
        for storage in state.storage:  # iterate through the storages
            #  (x1-y1) + (x2-y2)
            man_distances.append(abs(box[0] - storage[0]) + abs(box[1] - storage[1]))
            # print(man_distances)
        #     # add shortest manhattan distance to total dist
        man_heur += min(man_distances)
    return man_heur
    # a = [abs(box[0] - storage[0]) + abs(box[1] - storage[1]) for box in state.boxes for storage in
    #            state.storage]
    # print(a)


# [4, 6, 4, 2, 4, 2, 4, 6, 2, 4, 6, 4, 6, 4, 2, 4]

#
# return sum(min([abs(box[0] - storage[0]) + abs(box[1] - storage[1])]) for box in state.boxes for storage in
#            state.storage)


# SOKOBAN HEURISTICS
def trivial_heuristic(state):
    '''trivial admissible sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
    count = 0
    for box in state.boxes:
        if box not in state.storage:
            count += 1
    return count


def rm(box, state):
    """
    Empty the storage from other boxes that are occupying them...
    """
    # storages_list = fetch_storage(state)
    storages_list = [x for x in state.storage]
    box_list = list(state.boxes)

    for i in box_list:
        if i not in storages_list:
            continue
        else:
        # print([x for x in storages_list] == storages_list)
            if i in storages_list:
                if i != box:
                    storages_list.remove(i)
    # print([i  for i in box_list if i in storages_list2 if i!=box] == storages_list)

    # print(storages_list)
    # print([x for x in box_list if x in storages_list if box == x])
    return storages_list


def ch_dlock(position, state):
    """
    Check deadlocks
    """
    # check if the box is deadlocked
    obs = state.obstacles.union(state.boxes)
    oblist = list(obs)

    # (x, y) --> box positions, (x, y)
    up = (position[0], position[1] + 1)
    down = (position[0], position[1] - 1)
    left = (position[0] - 1, position[1])
    right = (position[0] + 1, position[1])
    return (position[0] == 0 and position[1] == 0) or (position[0] == 0 and up in oblist) or (position[0] == 0
                                                                                              and down in oblist) or (
                       position[0] == 0 and right in oblist) or (position[1] == 0 and position[0] == 0) \
           or (position[1] == 0 and left in oblist) or (position[1] == 0 and right in oblist) or \
           (position[1] == 0 and down in oblist) or \
           (position[0] == state.width - 1 and position[1] == state.height - 1) or \
           (position[0] == state.width - 1 and position[1] == 0) or (position[0] == state.width - 1 and left in oblist) \
           or (position[0] == state.width - 1 and up in oblist) or (position[0] == state.width - 1 and down in oblist) \
           or (position[1] == state.height - 1 and position[0] == state.width - 1) \
           or (position[1] == state.height - 1 and position[0] == 0) or (position[1] == state.height - 1 and left
                                                                         in oblist) or (
                       position[1] == state.height - 1 and right in oblist) or (position[1] == state.height - 1
                                                                                and up in oblist)


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

    obs = state.obstacles.union(state.robots)

    i = 0
    boxes = list(state.boxes)
    while i < len(boxes):
        storages = rm(boxes[i], state)
        if boxes[i] not in storages:
            if ch_dlock(boxes[i], state):
                return state_inf
            else:
                pass
        i += 1
    else:
        altn_heur = 0
        boxes = list(state.boxes)
        j = 0
        while j < len(boxes):
            cost = state_inf
            spaces = rm(boxes[j], state)
            k = 0
            while k < len(spaces):
                max_distx = max(boxes[j][0], spaces[k][0])
                min_distx = min(boxes[j][0], spaces[k][0])
                max_disty = max(boxes[j][1], spaces[k][1])
                min_disty = min(boxes[j][1], spaces[k][1])
                num_obs = sum(1 for x in obs if max_distx > x[0] > min_distx and max_disty > x[1] > min_disty)
                # iterate through all the spaces available
                curr_cost = abs(boxes[j][0] - spaces[k][0]) + abs(boxes[j][1] - spaces[k][1]) + num_obs * 2
                if curr_cost < cost:
                    cost = curr_cost
                else:
                    pass
                k += 1
            j += 1
            altn_heur += cost

        robots = list(state.robots)
        n = 0
        while n < len(robots):
            cost = state_inf
            boxes = list(state.boxes)
            m = 0
            while m < len(boxes):
                max_distx = max(robots[n][0], boxes[m][0])
                min_distx = min(robots[n][0], boxes[m][0])
                max_disty = max(robots[n][1], boxes[m][1])
                min_disty = min(robots[n][1], boxes[m][1])
                num_obs = sum(1 for x in obs if max_distx > x[0] > min_distx and max_disty > x[1] > min_disty)
                if abs(boxes[m][0] - robots[n][0]) + abs(boxes[m][1] - robots[n][1]) + num_obs < cost:
                    cost = abs(boxes[m][0] - robots[n][0]) + abs(boxes[m][1] - robots[n][1]) + num_obs * 2
                else:
                    pass
                m += 1
            n += 1
            altn_heur += cost

    # altermate heuristic => steps taken from robot to box, box to goal
    return altn_heur


def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0


def fval_function(sN, weight):
    # IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
    # Many searches will explore nodes (or states) that are ordered by their f-value.
    # For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    # You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    # The function must return a numeric f-value.
    # The value will determine your state's position on the Frontier list during a 'custom' search.
    # You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return (weight * sN.hval) + sN.gval


def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound=10):  # pruning
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    state_inf = float('inf')

    weight_fval = (lambda sN: fval_function(sN, weight))  # weight
    search_util = SearchEngine('custom', 'default')
    search_util.init_search(initial_state, sokoban_goal_state, heur_fn, weight_fval)

    time_start = os.times()[0]  # usertime
    end_time = time_start + timebound  # endtime
    final = search_util.search(timebound)

    # teaching labs, 16/20, 13 better than bench mark
    soln = False
    while time_start < end_time:
        if final is not False:
            cost_bound = (state_inf, state_inf, state_inf)
            time_passed = os.times()[0] - time_start
            timebound -= time_passed
            # weight *= 999

            # prune...
            if final.gval < cost_bound[0]:
                if weight > 1:  # must prune on the weight
                    weight /= 1.3
            cost_bound = (final.gval, final.gval, final.gval)
            soln = final
            final = search_util.search(timebound, cost_bound)
        else:
            break
    return soln


def anytime_gbfs(initial_state, heur_fn, timebound=10):  # pruning? on gval?
    # IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of anytime gbfs algorithm'''
    state_inf = float('inf')

    search_util = SearchEngine('best_first', 'default')
    search_util.init_search(initial_state, sokoban_goal_state, heur_fn)

    time_start = os.times()[0]  # user time
    end_time = time_start + timebound  # search end time_start
    final = search_util.search(timebound)  # start searching with the time bound

    # tested on teaching labs on feb 3rd 14:17 PM, 17 pass, 16 better than the benchmark
    soln = False
    while time_start < end_time:
        if final is not False:
            cost_bound = (state_inf, state_inf, state_inf)
            time_passed = os.times()[0] - time_start
            timebound -= time_passed

            gvalue = final.gval

            if gvalue < cost_bound[0]:
                gvalue -= 1  # prune on the gvalue
                soln = final
            cost_bound = (final.gval, final.gval, final.gval)
            final = search_util.search(timebound, cost_bound)  # time passed
        else:
            break
    return soln
# astar smaller than gbfs
# gvalues 16 5 21 10 8 36 16 41 14 90 35 30 33 31 29 80 void void void 158 gbfs
# gvalues 16 5 21 10 10

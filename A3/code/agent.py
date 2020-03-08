"""
An AI player for Othello.
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

# Minimax Hints: Use the get possible moves(board, color) function in othello shared.py, which returns a
# list of (column, row) tuples representing the legal moves for player color. Use the play move(board, color,
# move) function in othello shared.py, which computes the successor board state that results from player
# color playing move (a (column, row) tuple). Pay attention to which player should make a move for min
# nodes and max nodes at the beginning of each function. If a state is already in the dictionary and do not explore it again.
# The starter code is structured so that if you type $python3 othello gui.py -d 6 -a agent.py -m
# -c, the game manager will call your agent’s MINIMAX routines with the ’caching’ flag on. If instead you
# remove the -m and type $python3 othello gui.py -d 6 -a agent.py -c, the game manager will
# call your agent’s ALPHA-BETA routines with the ’caching’ flag on.

# 6. We can try to speed up the AI even more by caching states we’ve seen before. To do this, we will want to
# alter your program so that it responds to the -c flag at the command line. To implement state caching you
# will need to create a dictionary in your AI player (this can just be stored in a global variable on the top level
# of the file) that maps board states to their minimax value. Modify your minimax and alpha-beta pruning
# functions to store states in that dictionary after their minimax value is known. Then check the dictionary,

# 7. Alpha-beta pruning works better if nodes that lead to a better utility are explored first. To do this, in the
# Alpha-beta pruning functions, we will want to order successor states according to the following heuristic:
# the nodes for which the number of the AI player’s disks minus the number of the opponent’s disks is high-
# est should be explored first. Note that this is the same as the utility function, and it is okay to call the utility
# function to compute this value. This should provide another small speed-up.
# Alter your program so that it executes node ordering when the -o flag is placed on the command line. The
# starter code is already structured so that if you type $python3 othello gui.py -d 6 -a agent.py
# -o, the game manager will call your agent’s ALPHA-BETA routines with an ’ordering’ parameter that is
# equal to 1.

cached_params = {}

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)

# Method to compute utility value of terminal state
def compute_utility(board, color):
    """
    1. this is part of minimax, must write this first
    The function get score(board) returns a tuple (number of dark disks, number of light disks).
    :param board:
    :param color:
    :return:
    """
    #IMPLEMENT
    score = get_score(board)
    return score[0] - score[1] if color == 1 else score[1] - score[0]

# # Better heuristic value of board
# def compute_heuristic(board, color): #not implemented, optional
#     #IMPLEMENT
#     return 0 #change this!

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    """
    2. helper to implement recursive minimax
    :param board:
    :param color:
    :param limit:
    :param caching:
    :return:
    """
    other_color = 2 if color == 1 else 1

    moves = get_possible_moves(board, other_color)
    # print(all_moves)

    if len(moves) == 0 or limit == 0:
        return None, compute_utility(board, color)
    else:
        min_utility = float('inf')
        min_move = None

        # change to while
        for each in moves:

            move, new_utiltiy = minimax_max_node(play_move(board, other_color, each[0], each[1]), color, limit - 1)
            cached_params[play_move(board, other_color, each[0], each[1])] = (move, new_utiltiy)
                # print(cached_params)

            if new_utiltiy < min_utility:
                min_utility = new_utiltiy
                min_move = each

    return (min_move, min_utility)


def minimax_max_node(board, color, limit, caching = 0):
    """
    2. helper to implement recursive minimax
    :param board:
    :param color:
    :param limit:
    :param caching:
    :return:
    """
    moves = get_possible_moves(board, color)

    if len(moves) == 0 or limit == 0:
        return None, compute_utility(board, color)
    else:
        max_until = float('-inf')
        max_move = None

        for each in moves:
            move, new_until = minimax_min_node(play_move(board, color, each[0], each[1]), color, limit -1)
            cached_params[play_move(board, color, each[0], each[1])] = (move, new_until)

            if new_until > max_until:
                max_until = new_until
                max_move = each

    return (max_move, max_until)

def select_move_minimax(board, color, limit, caching = 0):
    """
    3. Write this function using compute utility
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  Use 1 and 2 recursively

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    #IMPLEMENT
    return minimax_max_node(board, color, limit)[0]

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    """
    4. helper for select_move_alphabeta
    :param board:
    :param color:
    :param alpha:
    :param beta:
    :param limit:
    :param caching:
    :param ordering:
    :return:
    """
    other_color = 2 if color == 1 else 1

    moves = get_possible_moves(board, other_color)

    if len(moves) == 0 or limit == 0:
        return None, compute_utility(board, color)
    else:
        min_utility = float('inf')
        min_move = None

        sorted_moves = [(each, play_move(board, other_color, each[0], each[1])) for each in moves]

        sorted_moves.sort(key=lambda util: compute_utility(util[1], color))

        for each in sorted_moves:

            move, new_until = alphabeta_max_node(each[1], color, alpha, beta, limit -1)
            cached_params[each[1]] = (move, new_until)

            if new_until < min_utility:
                min_utility = new_until
                min_move = each[0]

            if min_utility <= alpha:
                return min_move, min_utility

            if min_utility < beta:
                beta = min_utility

        return min_move, min_utility


def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    """
    4. helper for select_move_alphabeta
    :param board:
    :param color:
    :param alpha:
    :param beta:
    :param limit:
    :param caching:
    :param ordering:
    :return:
    """
    moves = get_possible_moves(board, color)

    if len(moves) == 0 or limit == 0:
        return None, compute_utility(board, color)
    else:
        max_utility = float('-inf')
        max_move = None

        sorted_moves = [(each, play_move(board, color, each[0], each[1])) for each in moves]

        sorted_moves.sort(key=lambda util: compute_utility(util[1], color), reverse=True)

        for each in sorted_moves:
            move, new_until = alphabeta_min_node(each[1], color, alpha, beta, limit -1)
            cached_params[each[1]] = (move, new_until)

            if new_until > max_utility:
                max_utility = new_until
                max_move = each[0]

            if max_utility >= beta:
                return max_move, max_utility

            if max_utility > alpha:
                alpha = max_utility

        return (max_move, max_utility)



def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    5. Implement, same way as selective_move_minimax

    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations.
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations.
    """
    alpha = float('-inf')
    beta = -1 * alpha
    return alphabeta_max_node(board, color, alpha, beta, limit)[0]




####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()

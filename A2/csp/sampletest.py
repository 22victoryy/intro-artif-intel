#
# from cspbase import *
# from propagators import *
# from futoshiki_csp import futoshiki_csp_model_1, futoshiki_csp_model_2
# import itertools
# import random
# import math
# inequalities = ["<", ">"]
# possible_cell = [*inequalities, "."]
#
#
# def pre_filled_domain(domain, board_size):
#     pre_filled = [i for i in range(1, board_size + 1)]
#     domain.extend(pre_filled)
#     return domain
#
# def get_free_domain(board_size, min_val=1):
#     free_domain = ["0", "."]
#     # free_domain.append(0)
#     return free_domain
#
# def get_board(board_size, pre_filled=False):
#     # board_size = int(math.sqrt(size))
#     domain = get_free_domain(board_size)
#     if pre_filled:
#         pre_filled_domain(domain, board_size)
#     # print(domain, possible_cell)
#     board = []
#     for row in range(board_size):
#         row = []
#         for col in range(board_size * 2 - 1):
#             domain_index = col % 2
#             # print("hello there!!", domain[domain_index])
#             row.append(domain[domain_index])
#         board.append(row)
#     return board
#
# if _name_ == "_main_":
#     # board = get_board(5)
#     board = [['0', '>', '1', '.', '0', '<', '0', '.', '0'], ['0', '.', '3', '>', '0', '.', '0', '.', '0'], ['0', '.', '0', '.',
#                                                                                                             '0', '<', '4', '.', '0'], ['0', '.', '0', '.', '0', '.', '0', '>', '0'], ['0', '.', '0', '.', '0', '<', '0', '.', '0']]
#     # print(board)
#     for row in board:
#         print(row)
#     futoshiki, vars = futoshiki_csp_model_1(board)
#     # futoshiki, vars = futoshiki_csp_model_2(board)
#     # futoshiki.print_all()
#     btracker = BT(futoshiki)
#     # btracker.trace_on()
#
#     # print("Plain Bactracking on futoshiki CSP")
#     # btracker.bt_search(prop_BT, ord_mrv)
#     print("=======================================================")
#     print("Forward Checking on futoshiki CSP")
#     btracker.bt_search(prop_FC, ord_mrv)
#     print("hellllo", vars[0][0].get_assigned_value())
#     print("=======================================================")
#     print("GAC on futoshiki CSP")
#     btracker.bt_search(prop_GAC, ord_mrv)
#     print("=======================================================")

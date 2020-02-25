#Look for #IMPLEMENT tags in this file.
# Do this later
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.


For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary
      all-different constraints for both the row and column constraints.

'''
from cspbase import *
from propagators import *
import itertools


# Domain, variables, constraints
    # 1. Define variables
    # 2. Define constraints
    # 3. Add to the csp
    # cspbase.py contains the variable class, and the constraint class
    # use variable class to define the variables,
    # use constraint class define the constraints
    # add to the csp --> last step



def futoshiki_csp_model_1(futo_grid):
    """
    A Futoshiki Model takes as input a Futoshiki board, and returns a CSP object, consisting of a variable
    corresponding to each cell of the board.

    The variable domain of that cell is {1,...,n} if the board is unfilled at that position, and equal to i if the
    board has a fixed number i at that cell.

   All appropriate constraints will be added to the board as well.
    """
    rows = len(futo_grid)
    cols = len(futo_grid[0])

    domain = [i + 1 for i in range(rows)]

    variables = []
    var_array = []

    j = 0
    while j < len(range(rows)):
        row = []
        k = 0
        while k < len(range(cols)):

            if k % 2 == 0 and futo_grid[j][k] == 0:
                var = Variable("{}{}".format(j, k // 2), domain)
                row.append(var)
                variables.append(var)
            elif k % 2 == 0 and futo_grid[j][k] != 0:
                fixed = [futo_grid[j][k]]
                var = Variable("{}{}".format(j, k // 2), fixed)
                row.append(var)
                variables.append(var)
            k += 1
        var_array.append(row)
        j += 1

    constraints = []

    a = 0
    while a < len(var_array):
        b = 0
        while b < len(var_array):

            c = b + 1
            while c in range(b + 1, len(var_array)):

                row_cons = Constraint("{}{},{}{}".format(a, b, a, c), [var_array[a][b], var_array[a][c]])
                col_cons = Constraint("{}{},{}{}".format(b, a, c, a), [var_array[b][a], var_array[c][a]])
                satisfied = []

                for it in itertools.product(var_array[a][b].cur_domain(), var_array[a][c].cur_domain()):

                    if it[0] != it[1]:
                        satisfied.append(it)

                for it in itertools.product(var_array[b][a].cur_domain(), var_array[c][a].cur_domain()):

                    if it[0] != it[1]:
                        satisfied.append(it)

                row_cons.add_satisfying_tuples(satisfied)
                constraints.append(row_cons)

                col_cons.add_satisfying_tuples(satisfied)
                constraints.append(col_cons)
                c += 1
            b += 1
        a += 1

    csp = CSP("{}x{}".format(len(var_array), len(var_array)), variables)

    for c in constraints:
        csp.add_constraint(c)  # Add the constraints to the csp

    return csp, var_array

def futoshiki_csp_model_2(futo_grid):
    """
    :param futo_grid:
    :type futo_grid:
    :return:
    :rtype:
    """
    rows = len(futo_grid)
    cols = len(futo_grid[0])

    # domain
    domain = [i + 1 for i in range(rows)]

    variables = []
    var_array = []  # get the assigned value from var_array
    alldiff = []

    j = 0
    while j < len(range(rows)):
        row = []
        diff = []
        k = 0
        while k < len(range(cols)):
            if k % 2 == 0:
                if futo_grid[j][k] == 0:
                    var = Variable("{}{}".format(j, k // 2), domain)
                else:
                    fixed = [futo_grid[j][k]]
                    var = Variable("{}{}".format(j, k // 2), fixed)

                row.append(var)
                variables.append(var)
            else:
                diff.append(futo_grid[j][k])
            k += 1
        alldiff.append(diff)
        var_array.append(row)
        j += 1

    constraints = []

    x = 0
    while x < len(var_array):
        row_vars = list(var_array[x])
        col_vars = []
        y = 0
        while y < len(var_array):
            if y < len(alldiff[x]):

                # create binary constraints between variables that have an inequality
                if alldiff[x][y] != '.':
                    con = Constraint("{}{},{}{}".format(x, y, x, y + 1), [var_array[x][y], var_array[x][y + 1]])

                    # different scope
                    set_tuples = []
                    for t in itertools.product(var_array[x][y].cur_domain(), var_array[x][y + 1].cur_domain()):
                        if not (alldiff[x][y] == '<' or alldiff == '>'):
                            set_tuples.append(t)

                    con.add_satisfying_tuples(set_tuples)
                    constraints.append(con)
            y += 1

        con_row = Constraint("Row{}".format(x), row_vars)

        con.add_satisfying_tuples(set_tuples)
        constraints.append(con_row)

        con_col = Constraint("Col{})".format(x), col_vars)

        con.add_satisfying_tuples(set_tuples)
        constraints.append(con_col)

        x += 1

    csp = CSP("{}x{}".format(len(var_array), len(var_array)), variables)

    for c in constraints:
        csp.add_constraint(c)

    return csp, var_array



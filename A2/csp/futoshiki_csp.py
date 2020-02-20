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

def futoshiki_csp_model_1(futo_grid):
    """
    :param futo_grid:
    :type futo_grid:
    :return:
    :rtype:
    """
    ##IMPLEMENT
    # print(futo_grid)
    # Create Variable Objects
    vs = []
    var_array = []
    inequality_array = []
    num_rows = len(futo_grid)
    num_cols = 0

    if num_rows > 0:
        num_cols = len(futo_grid[0])

    # domain if Variable is 0 initially
    
    dom = []
    for i in range(num_rows):
        dom.append(i + 1)

    for i in range(num_rows):
        row = []
        row_inequality = []
        for j in range(num_cols):
            if j % 2 == 0:
                if futo_grid[i][j] == 0:
                    var = Variable("V{}{}".format(i, j // 2), dom)
                else:  # cell has fixed value
                    fixed = [futo_grid[i][j]]
                    var = Variable("V{}{}".format(i, j // 2), fixed)

                row.append(var)
                vs.append(var)

            else:
                row_inequality.append(futo_grid[i][j])

        inequality_array.append(row_inequality)
        var_array.append(row)

    # Create Constraint objects for the model
    cons = []
    n = len(var_array)

    for i in range(n):
        for j in range(n):
            for x in range(j + 1, n):
                # row constraints
                var1 = var_array[i][j]
                var2 = var_array[i][x]
                con = Constraint("C(V{}{},V{}{})".format(i, j, i, x), [var1, var2])
                sat_tuples = []
                for t in itertools.product(var1.cur_domain(), var2.cur_domain()):
                    if checker(inequality_array[i][j], (i, j), (i, x), t[0], t[1]):
                        sat_tuples.append(t)

                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

                # column constraints

                var1 = var_array[j][i]
                var2 = var_array[x][i]
                con = Constraint("C(V{}{},V{}{})".format(j, i, x, i), [var1, var2])
                sat_tuples = []
                for t in itertools.product(var1.cur_domain(), var2.cur_domain()):
                    if checker('.', (j, i), (x, i), t[0], t[1]):
                        sat_tuples.append(t)

                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    csp = CSP("{}x{}-futoshiki".format(n, n), vs)

    for c in cons:
        csp.add_constraint(c)

    return csp, var_array


def futoshiki_csp_model_2(futo_grid):
    """
    :param futo_grid:
    :type futo_grid:
    :return:
    :rtype:
    """
    # Create Variable Objects
    vs = []
    var_array = []
    inequality_array = []
    num_rows = len(futo_grid)

    if num_rows > 0:
        num_cols = len(futo_grid[0])

    # domain if Variable is 0 initially
    dom = []
    for i in range(num_rows):
        dom.append(i + 1)

    for i in range(num_rows):
        row = []
        row_inequality = []
        for j in range(num_cols):
            if j % 2 == 0:
                if futo_grid[i][j] == 0:
                    var = Variable("V{}{}".format(i, j // 2), dom)
                else:  # cell has fixed value
                    fixed = [futo_grid[i][j]]
                    var = Variable("V{}{}".format(i, j // 2), fixed)

                row.append(var)
                vs.append(var)

            else:
                row_inequality.append(futo_grid[i][j])

        inequality_array.append(row_inequality)
        var_array.append(row)

    # Create Constraint objects for the model
    cons = []
    n = len(var_array)

    # rows
    for i in range(n):
        row_vars = list(var_array[i])
        col_vars = []
        col_var_doms = []
        row_var_doms = []
        for j in range(n):
            # get domains of all vs in the same row
            row_var_doms.append(var_array[i][j].cur_domain())

            # collect colunm vs and there respective domains
            col_vars.append(var_array[j][i])
            col_var_doms.append(var_array[j][i].cur_domain())

            # create binary inequality constraints
            if j < len(inequality_array[i]):
                var1 = var_array[i][j]
                var2 = var_array[i][j + 1]

                # if statement is used in order to create binary constraints
                # between variables that have an inequality
                if inequality_array[i][j] != '.':
                    con = Constraint("C(V{}{},V{}{})".format(i, j, i, j + 1), [var1, var2])
                    sat_tuples = []
                    for t in itertools.product(var1.cur_domain(), var2.cur_domain()):
                        if inequality_checker(inequality_array[i][j], t[0], t[1]):
                            sat_tuples.append(t)

                    con.add_satisfying_tuples(sat_tuples)
                    cons.append(con)

        # create all-diff row constraint
        con = Constraint("C(Row-{})".format(i), row_vars)
        sat_tuples = []
        for t in itertools.product(*row_var_doms):
            if all_diff_checker(row_vars, t):
                sat_tuples.append(t)

        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

        # create all-diff column constraints
        con = Constraint("C(Col-{})".format(i), col_vars)
        sat_tuples = []
        for t in itertools.product(*col_var_doms):
            if all_diff_checker(col_vars, t):
                sat_tuples.append(t)

        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    csp = CSP("{}x{}-futoshiki".format(n, n), vs)

    for c in cons:
        csp.add_constraint(c)

    return csp, var_array


def checker(inequality, var1_tup, var2_tup, val1, val2):
    """
    :param inequality:
    :type inequality:
    :param var1_tup:
    :type var1_tup:
    :param var2_tup:
    :type var2_tup:
    :param val1:
    :type val1:
    :param val2:
    :type val2:
    :return:
    :rtype:
    """

    result = val1 != val2

    # check if var1 and var2 are adjacent cells
    if var1_tup[1] + 1 == var2_tup[1]:

        result = result and inequality_checker(inequality,val1,val2)

    return result


def inequality_checker(inequality, val1, val2):
    """
    :param inequality:
    :type inequality:
    :param val1:
    :type val1:
    :param val2:
    :type val2:
    :return:
    :rtype:
    """
    result = True

    if inequality == '<':
      result = (val1 < val2)

    elif inequality == '>':
      result = (val1 > val2)

    return result

def all_diff_checker(v, vals):
    """
    s
    """
    result = True
    for i in range(len(v)):
      for j in range(i+1, len(v)):
        result = result and (vals[i] != vals[j])

    return result




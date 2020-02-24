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
    cols = 0

    # define the space
    if rows >= 0:
        cols = len(futo_grid[0])

    # increments domain for the rows
    domain = []
    i = 0
    while i < len(range(rows)):
        domain.append(i + 1)
        i += 1

    variables = []
    var_array = [] # get the assigned value from var_array

    j = 0
    while j < len(range(rows)):
        row = []
        # inq = []
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

#####################################################################################################################

    # Create Constraint objects for the model
    constraints = []
    n = len(var_array)

    for i in range(n):
        for j in range(n):
            for x in range(j + 1, n):

                # row constraints
                row_var1 = var_array[i][j]
                row_var2 = var_array[i][x]

                col_var1 = var_array[j][i]
                col_var2 = var_array[x][i]

                row_cons = Constraint("{}{},{}{}".format(i, j, i, x), [row_var1, row_var2])
                col_cons = Constraint("{}{},{}{}".format(j, i, x, i), [col_var1, col_var2])

                set_tuples = []

                # iterate over two objects
                for t in itertools.product(row_var1.cur_domain(), row_var2.cur_domain()):

                    if t[0] != t[1]:
                        set_tuples.append(t)

                for t in itertools.product(col_var1.cur_domain(), col_var2.cur_domain()):

                    if t[0] != t[1]:
                        set_tuples.append(t)

                row_cons.add_satisfying_tuples(set_tuples)
                constraints.append(row_cons)

                col_cons.add_satisfying_tuples(set_tuples)
                constraints.append(col_cons)

    csp = CSP("{}x{}".format(n, n), variables)
    # print(variables)

    for c in constraints:
        csp.add_constraint(c)  # Add the constraints to the csp

    return csp, var_array

################################################################################################################

def futoshiki_csp_model_2(futo_grid):
    """
    :param futo_grid:
    :type futo_grid:
    :return:
    :rtype:
    """
    rows = len(futo_grid)
    cols = 0

    # define the space
    if rows >= 0:
        cols = len(futo_grid[0])

    # increments domain for the rows
    # do stuff for the variables and constraints
    domain = []
    i = 0
    while i < len(range(rows)):
        domain.append(i + 1)
        i += 1

    variables = []
    var_array = []  # get the assigned value from var_array
    inq_arr = []

    j = 0
    while j < len(range(rows)):
        row = []
        inq = []
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
                inq.append(futo_grid[j][k])
            k += 1
        inq_arr.append(inq)
        var_array.append(row)
        j += 1

    # Create Constraint objects for the model
    constraints = []
    n = len(var_array)


    for i in range(n):
        row_vars = list(var_array[i])
        col_vars = []

        for j in range(n):

            # create binary inequality constraints
            if j < len(inq_arr[i]):
                var1 = var_array[i][j]
                var2 = var_array[i][j + 1]

                # create binary constraints between variables that have an inequality
                if inq_arr[i][j] != '.':
                    con = Constraint("C(V{}{},V{}{})".format(i, j, i, j + 1), [var1, var2])
                    # different scope
                    set_tuples = []
                    for t in itertools.product(var1.cur_domain(), var2.cur_domain()):
                        if not (inq_arr[i][j] == '<' or inq_arr == '>'):
                            set_tuples.append(t)

                    con.add_satisfying_tuples(set_tuples)
                    constraints.append(con)

        # create all-diff row constraint
        con_row = Constraint("C(Row-{})".format(i), row_vars)

        con.add_satisfying_tuples(set_tuples)
        constraints.append(con_row)

        # create all-diff column constraints
        con_col = Constraint("C(Col-{})".format(i), col_vars)


        con.add_satisfying_tuples(set_tuples)
        constraints.append(con_col)

    csp = CSP("{}x{}".format(n, n), variables)

    for c in constraints:
        csp.add_constraint(c)

    return csp, var_array

##############################################################################################################

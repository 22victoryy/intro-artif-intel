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
import itertools

# Domain, variables, constraints
    # 1. Define variables
    # 2. Define constraints
    # 3. Add to the csp
    # cspbase.py contains the variable class, and the constraint class
    # use variable class to define the variables,
    # use constraint class define the constraints

# Structure from propagators_test.py
#
# '''Return an n-queens CSP'''
#     i = 0
#     dom = []
#     for i in range(n):
#         dom.append(i+1)
#
#     vars = []
#     for i in dom:
#         vars.append(Variable('Q{}'.format(i), dom))
#
#     cons = []
#     for qi in range(len(dom)):
#         for qj in range(qi+1, len(dom)):
#             con = Constraint("C(Q{},Q{})".format(qi+1,qj+1),[vars[qi], vars[qj]])
#             sat_tuples = []
#             for t in itertools.product(dom, dom):
#                 if queensCheck(qi, qj, t[0], t[1]):
#                     sat_tuples.append(t)
#             con.add_satisfying_tuples(sat_tuples)
#             cons.append(con)
#
#     csp = CSP("{}-Queens".format(n), vars)
#     for c in cons:
#         csp.add_constraint(c)
#     return csp

def futoshiki_csp_model_1(futo_grid):
    """
    A Futoshiki Model takes as input a Futoshiki board, and returns a CSP object, consisting of a variable
    corresponding to each cell of the board.

    The variable domain of that cell is {1,...,n} if the board is unfilled at that position, and equal to i if the
    board has a fixed number i at that cell.

   All appropriate constraints will be added to the board as well.
   variable array --> [[v1, v2, v3],[v1, v2, v3],[v1, v2, v3]]
    """
    grid = len(futo_grid)

    variables = []
    var_array = []
    alldiff = []

    csp = CSP('futoshiki_model_2')

    domain = [i + 1 for i in range(grid)]

    j = 0
    while j < len(range(0, grid)):
        row = []
        diff = []
        k = 0

        while k < len(range(0, len(futo_grid[j]))):
            if futo_grid[j][k] == 0:
                var = Variable("{}{}".format(j, k), domain)
                csp.add_var(var)
                row = [*row, var]
                variables = [*variables, var]
            elif k % 2 == 0 and futo_grid[j][k] != 0:
                var = Variable("{}{}".format(j, k), [futo_grid[j][k]])
                csp.add_var(var)
                row = [*row, var]
                variables = [*variables, var]
            else:
                diff = [*diff, futo_grid[j][k]]
            k += 1
        alldiff = [*alldiff, diff]
        var_array = [*var_array, row]
        j += 1
    # print(type(var_array[0][0]))
    print(variables)
    # print(var_array)


    a = 0
    while a  < len(var_array):
        b = 0
        while b < len(var_array):
            c = b + 1
            while c in range(b + 1, len(var_array)):

                if alldiff[a][b] == '<':
                    greater = Constraint('{}{},{}{}'.format(a, b, a, c + 1), [var_array[a][b], var_array[a][c]])
                    greater_tuples = [it for it in itertools.product(var_array[a][b].domain(), var_array[a][c].domain()) if it[0] < it[1]]
                    greater.add_satisfying_tuples(greater_tuples)
                    csp.add_constraint(greater)

                elif alldiff[a][b] == '>':
                    less = Constraint('{}{},{}{}'.format(a, b, a, c + 1), [var_array[a][b], var_array[a][c]])
                    less_tuples = [it for it in itertools.product(var_array[a][b].domain(), var_array[a][c].domain()) if it[0] > it[1]]
                    less.add_satisfying_tuples(less_tuples)
                    csp.add_constraint(less)

                row_cons = Constraint("{}{},{}{}".format(a, b, a, c + 1), [var_array[a][b], var_array[a][c]])
                col_cons = Constraint("{}{},{}{}".format(b, a, c, a + 1), [var_array[b][a], var_array[c][a]])

                satisfied_row = [it for it in itertools.product(var_array[a][b].cur_domain(),
                                                                var_array[a][c].cur_domain()) if it[0] != it[1]]

                satisfied_column = [it for it in itertools.product(var_array[b][a].cur_domain(),
                                                                   var_array[c][a].cur_domain()) if it[0] != it[1]]

                satisfied = satisfied_row + satisfied_column
                row_cons.add_satisfying_tuples(satisfied)
                col_cons.add_satisfying_tuples(satisfied)

                csp.add_constraint(row_cons)
                csp.add_constraint(col_cons)
                c += 1
            b += 1
        a += 1

    # test script return type: csp, var_array
    return csp, var_array


def futoshiki_csp_model_2(futo_grid):
    """
    :param futo_grid:
    :type futo_grid:
    :return:
    :rtype:
    """
    grid = len(futo_grid)

    variables = []
    var_array = []
    alldiff = []

    csp = CSP('futoshiki_model_2')

    domain = [i + 1 for i in range(grid)]

    j = 0
    while j < len(range(0, grid)):
        row = []
        diff = []
        k = 0

        while k < len(range(0, len(futo_grid[j]))):
            if futo_grid[j][k] == 0:
                var = Variable("{}{}".format(j, k), domain)
                csp.add_var(var)
                row = [*row, var]
                variables = [*variables, var]
            elif k % 2 == 0 and futo_grid[j][k] != 0:
                var = Variable("{}{}".format(j, k), [futo_grid[j][k]])
                csp.add_var(var)
                row = [*row, var]
                variables = [*variables, var]
            else:
                diff = [*diff, futo_grid[j][k]]
            k += 1
        alldiff = [*alldiff, diff]
        var_array = [*var_array, row]
        j += 1

    print(var_array)

    a = 0
    while a < len(var_array):
        b = 0
        while b < len(var_array):

            if b < len(alldiff[a]) and alldiff[a][b] != '.':
                inq_constraint = Constraint("[{}{}],[{}{}]".format(a, b, a, b + 1), [var_array[a][b], var_array[a][b + 1]])
                inq_tuples = [t for t in itertools.product(var_array[a][b].cur_domain(), var_array[a][b + 1].
                                                           cur_domain()) if t[0]!=t[1]]

                inq_constraint.add_satisfying_tuples(inq_tuples)
                csp.add_constraint(inq_constraint)

            if b < len(alldiff[a]) and alldiff[a][b] == '<':
                inq_constraint = Constraint("[{}{}],[{}{}]".format(a, b, a, b + 1), [var_array[a][b], var_array[a][b + 1]])
                greater_tuples = [t for t in itertools.product(var_array[a][b].cur_domain(), var_array[a][b + 1].
                                                           cur_domain()) if t[0] < t[1]]

                inq_constraint.add_satisfying_tuples(greater_tuples)
                csp.add_constraint(inq_constraint)

            if b < len(alldiff[a]) and alldiff[a][b] == '>':
                inq_constraint = Constraint("[{}{}],[{}{}]".format(a, b, a, b + 1), [var_array[a][b], var_array[a][b + 1]])
                less_tuples = [t for t in itertools.product(var_array[a][b].cur_domain(), var_array[a][b + 1].
                                                           cur_domain()) if t[0] > t[1]]
                inq_constraint.add_satisfying_tuples(less_tuples)
                csp.add_constraint(inq_constraint)
            b += 1

        for row in range(len(var_array)):
            row_con = Constraint('{}'.format(row), var_array[row])

            row_tuples = [it for it in itertools.permutations(domain, len(var_array)) for col in range(len(var_array))
                          if it[col] in var_array[row][col].domain()]

            row_con.add_satisfying_tuples(row_tuples)
            csp.add_constraint(row_con)

        for column in range(len(var_array)):
            col_con = Constraint('{}'.format(column), [i[column] for i in var_array])

            col_tuples = [it for it in itertools.permutations(domain, len(var_array))
                          for row in range(len(var_array)) if it[row] in var_array[row][column].domain()]

            col_con.add_satisfying_tuples(col_tuples)
            csp.add_constraint(col_con)
        a += 1

    return csp, var_array


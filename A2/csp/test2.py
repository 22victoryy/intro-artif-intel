from __future__ import print_function;
import random;

rse = "print('NopeNopeNope')";
random.seed(rse);
from cspbase import *
import propagators;
import futoshiki_csp;

# propagators.prop_BT
# propagators.prop_FC
# propagators.prop_GAC


def test_1x1(model):
    print("Testing empty 1x1 board...", end='');
    puzzle = [[0]];
    csp, vars = model(puzzle);
    if len(vars) != 1:
        return "Incorrect number of variables returned";
    if len(csp.vars) != 1:
        return "Incorrect number of variables in csp";
    if vars[0][0] != csp.vars[0]:
        return "Variables returned and CSP variables do not match";

    return "Passed";


def test_1x1_2(model):
    print("Testing 1x1 board with given number...", end='');
    puzzle = [[1]];
    csp, vars = model(puzzle);
    if len(vars) != 1:
        return "Incorrect number of variables returned";
    if len(csp.vars) != 1:
        return "Incorrect number of variables in csp";
    if vars[0][0] != csp.vars[0]:
        return "Variables returned and CSP variables do not match";
    if 1 not in vars[0][0].cur_domain():
        return "Domain does not contain 1";
    if len(vars[0][0].cur_domain()) > 1:
        return "Too many values in domain";

    return "Passed";


def test_2x2_1(model):
    print("Testing 2x2 empty board...", end='');
    puzzle = [[0, '.', 0], [0, '.', 0]];
    csp, vars = model(puzzle);
    if len(vars) != 2 or len(vars[0]) != 2 or len(vars[1]) != 2:
        return "Incorrect number of variables returned";
    if len(csp.vars) != 4:
        return "Incorrect number of variables in csp";
    if vars[0][0] != csp.vars[0]:
        return "Variables returned and CSP variables do not match";
    for v in filter(lambda v: len(v.cur_domain()) > 2, csp.get_all_vars()):
        return "Too many values in domain of " + v.name;

    return "Passed";


def test_7x7(model):
    print("Testing 7x7 empty board...", end='');
    puzzle = [([0, '.'] * 7)[:-1] for x in range(7)];
    csp, vars = model(puzzle);
    if len(vars) != 7 or any(map(lambda vs: len(vs) != 7, vars)):
        return "Incorrect number/shape of variables returned";
    if len(csp.vars) != 7 * 7:
        return "Incorrect number of variables in csp";

    btracker = BT(csp);
    btracker.bt_search(propagators.prop_GAC);

    for row in vars:
        assigned = [v.get_assigned_value() for v in row];
        for i in range(1, 8):
            if i not in assigned:
                return "Invalid assignment, row uniqueness violated";
    for j in range(7):
        assigned = [];
        for i in range(7):
            assigned += [vars[j][i].get_assigned_value()];
        for i in range(1, 8):
            if i not in assigned:
                return "Invalid assignment, column uniqueness violated";
    return "Passed";


def test_with_constraints(model=futoshiki_csp.futoshiki_csp_model_1, prop=propagators.prop_BT, size=5, num_givens=0,
                          num_constraints=10, seed=rse):
    print("------------------------------------------------------------------------------------------");
    print("Testing model={}, prop={}, {}x{} {}-constraint board...".format(model.__name__, prop.__name__, size, size,
                                                                           num_constraints));
    if num_givens > size * size or num_constraints > (size - 1) * (size):
        exec(rse);
        return "Failed to generate board.";
    random.seed(seed);
    puzzle = [([0, '.'] * size)[:-1] for x in range(size)];
    for i in range(num_givens):
        while True:
            x = random.randint(0, size - 1);
            y = random.randint(0, size - 1);
            if puzzle[y][2 * x] == 0:
                puzzle[y][2 * x] = random.randint(1, size);
                break;
    constraints = [];
    for i in range(num_constraints):
        while True:
            x = random.randint(0, size - 2);
            y = random.randint(0, size - 1);
            if puzzle[y][2 * x + 1] == '.':
                sym = random.choice('< >'.split());
                puzzle[y][2 * x + 1] = sym;
                constraints.append(((y, x), sym, (y, x + 1)));
                break;
    print("Puzzle=", puzzle);
    csp, vars = model(puzzle);
    if len(vars) != size or any(map(lambda vs: len(vs) != size, vars)):
        return "Incorrect number/shape of variables returned";
    if len(csp.vars) != size * size:
        return "Incorrect number of variables in csp";
    t0 = time.time()
    btracker = BT(csp);
    btracker.bt_search(propagators.prop_GAC);
    t1 = time.time()
    time_difference = t1 - t0

    if all((v.is_assigned() for v in csp.get_all_vars())):
        for row in vars:
            assigned = [v.get_assigned_value() for v in row];
            for i in range(1, size + 1):
                if i not in assigned:
                    return "Invalid assignment, row uniqueness violated";
        for j in range(size):
            assigned = [];
            for i in range(size):
                assigned += [vars[j][i].get_assigned_value()];
            for i in range(1, size + 1):
                if i not in assigned:
                    return "Invalid assignment, column uniqueness violated";

        for c in constraints:
            if c[1] == '<':
                if vars[c[0][0]][c[0][1]].get_assigned_value() >= vars[c[2][0]][c[2][1]].get_assigned_value():
                    return "Violated constraint {}".format(c);
            if c[1] == '>':
                if vars[c[0][0]][c[0][1]].get_assigned_value() <= vars[c[2][0]][c[2][1]].get_assigned_value():
                    return "Violated constraint {}".format(c);
    else:
        return "CSP could not be solved - indeterminate";
    print('The time difference for {} and {} is:'.format(model, prop))
    print(time_difference)
    return time_difference;


models = [futoshiki_csp.futoshiki_csp_model_1, futoshiki_csp.futoshiki_csp_model_2]
propagator_types = [propagators.prop_FC, propagators.prop_GAC]
t4 = time.time()
for m in models:
    for p in propagator_types:
        info_list = []
        info_list.append(test_with_constraints(m, p, size=5, num_givens=4, num_constraints=3))

        if p == propagator_types[0] and m == models[0]:
            # time, variable assignments, pruned variables tupple lists for 6 tests by using FC
            FC_info_list_m1 = list(info_list)
            print(FC_info_list_m1)
        if p == propagator_types[1] and m == models[0]:
            # time, variable assignments, pruned variables tupple lists for 6 tests by using GAC
            GAC_info_list_m1 = list(info_list)
            print(GAC_info_list_m1)
        # if p == propagator_types[2] and m == models[0]:
        #    #time, variable assignments, pruned variables tupple lists for 6 tests by using BT
        #    BT_info_list_m1 = list(info_list)
        #    print(BT_info_list_m1)
        if p == propagator_types[0] and m == models[1]:
            # time, variable assignments, pruned variables tupple lists for 6 tests by using FC
            FC_info_list_m2 = list(info_list)
            print(FC_info_list_m2)
        if p == propagator_types[1] and m == models[1]:
            # time, variable assignments, pruned variables tupple lists for 6 tests by using GAC
            GAC_info_list_m2 = list(info_list)
            print(GAC_info_list_m2)


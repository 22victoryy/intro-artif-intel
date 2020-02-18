#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

from collections import deque

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def FC_Check(constraint, variable, pruned):
    """
    Forward checking helper function that checks if var satisfies the constraints.
    Otherwise, prune the var and add to the prune list.
    """
    DWO = False
    for var in variable.cur_domain():
        if not constraint.has_support(variable, var):
            pruned.append((variable, var))
            variable.prune_value(var)
    if variable.cur_domain_size() == 0:
        return DWO, pruned
    return True, pruned

    # finished helper function


def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    #IMPLEMENT
    # # ok  = False
    pruned = []

    # for new variables, if var in scope and unassigned is 1
    if not newVar:
        for constraint in csp.get_all_cons():
            if constraint.get_n_unasgn() == 1:
                FC_Check(constraint, constraint.get_unasgn_vars()[0], pruned)

        # return False, pruned
    else:
        for constraint in csp.get_cons_with_var(newVar):
            if constraint.get_n_unasgn() == 1:
               FC_Check(constraint, constraint.get_unasgn_vars()[0], pruned)
                # DWO for var in constraint, return False and pruned for restore
                # if ok == False:
                #     return False, pruned
        # else:
        #     return True, pruned


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT
    c_queue = []
    pruned = []

    if not newVar:
        for c in csp.get_all_cons():
            c_queue.append(c)
    else:
        for c in csp.get_cons_with_var(newVar):
            c_queue.append(c)

    GAC_Enforce(csp, c_queue, pruned)



def GAC_Enforce(csp, c_queue, pruned):
    """
    Prune values through the GAC queue
    # """

    DWO = False
    while len(c_queue) != 0:
        c = c_queue.pop()
        for v in c.get_unasgn_vars():
            for d in v.cur_domain():
                if not c.has_support(v, d):
                    pruned.append((v, d))
                    v.prune_value(d)

                    if v.cur_domain_size == 0:
                        c_queue.clear()
                        return DWO, pruned
                    else:
                        for c_ in csp.get_cons_with_var(v):
                            if c_ not in c_queue:
                                c_queue.append(c_)
    return True, pruned






def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    """
    ord mrv returns the variable with the most constrained current domain
    """
    #IMPLEMENT
    min_size = float('inf')
    mrv = None
    for var in csp.get_all_unasgn_vars():
        if var.cur_domain_size() < min_size:
            min_size = var.cur_domain_size()
        mrv = var
    return mrv







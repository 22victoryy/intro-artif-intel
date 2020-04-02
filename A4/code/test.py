for f in factors:
    restrict_vars = v_intersect.intersection(f.get_scope())
    if len(restrict_vars) > 0:  # f can be restricted
        ff = f
        for ef in restrict_vars:
            ff = restrict_factor(ff, ef, ef.get_evidence())
        evar_list.append(ff)
    else:
        evar_list.append(f)

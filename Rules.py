# FUNZIONE CHE RITORNA TUTTI I CAMMINI DALLA RADICE ALLE FOGLIE ==> RULES
def all_rules(tr):
    rules = []
    paths = []
    find_rules(tr, rules, paths, 0, False, None)
    return paths


def find_rules(tr, path, paths, pathLen, append, value=None):
    if tr is None:
        return
    if append:
        if len(path) > pathLen:
            path[pathLen] = value
        else:
            path.append(value)

        pathLen = pathLen + 1
        if not isinstance(tr, dict):
            # trovata la foglia
            path.append(tr)
            pathLen = pathLen + 1
            path_rule = save_rule(path, pathLen)
            paths.append(path_rule)
            path.pop()
        else:
            for key in tr.keys():
                value = key
                find_rules(tr[key], path, paths, pathLen, True, value)
                if path:
                    path.pop()
    else:
        for key in tr.keys():
            value = key
            find_rules(tr[key], path, paths, pathLen, True, value)


# SALVA IL ROOT-TO-LEAF PATH
def save_rule(ints, end):
    nodes = []
    for i in ints[0: end]:
        nodes.append(i)
    return nodes

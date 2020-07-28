import copy
import DT
import Utilities

from timeit import default_timer as timer

# funzione che ritorna tutti i cammini dalla radice alla foglia cioè le rules
def all_rules(tr):
    rules = []
    paths = []
    # paths_final = []
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

        if isinstance(tr, DT.Leaf):
            path.append(tr.result)
            pathLen = pathLen + 1
            path_rule = save_rule(path, pathLen)
            paths.append(path_rule)
            path.pop()

        else:
            for keys in tr.branches.keys():
                value = [tr.attr, keys[1], keys[2]]

                find_rules(tr.get(keys[1], keys[2]), path, paths, pathLen, True, value)
                if path:
                    path.pop()
    else:
        for keys in tr.branches.keys():
            value = [tr.attr, keys[1], keys[2]]
            find_rules(tr.get(keys[1], keys[2]), path, paths, pathLen, True, value)


# salva il root-to-leaf path
def save_rule(ints, end):
    nodes = []
    for i in ints[0: end]:
        nodes.append(i)
    return nodes


# metodo generale che si occupa del pruning
def pruning(rules, validation_set, training_set):
    improved = True
    accuracy = Utilities.allrule_accuracy(rules, validation_set)
    pruned_acc = accuracy
    count = 0
    while improved:
        count = count + 1
        rules, pruned_acc, improved = prune(validation_set, rules, pruned_acc)
        # termino il pruning se l'accuratezza sul validation set supera quella sul training set
        accuracy_training_set = Utilities.allrule_accuracy(rules, training_set)
        if pruned_acc >= accuracy_training_set:
            improved = False
    print('il numero di potature è :', count)
    return [accuracy, rules, pruned_acc]


# per ciascuna regola prova a eliminare un valore e calcola l'accuracy
def prune(prune_set, rules, accuracy):
    tmp_rules = copy.deepcopy(rules)
    list_tmp_values = []
    improved = False
    max_accuracy = accuracy
    start = timer()
    for i in rules:
        idx_rule = rules.index(i)  # indice della regola in copy_rules
        position_target = len(i) - 1
        for index in i[:position_target]:  # ciclo su tutti gli elementi e provo a potarne uno alla volta
            start1 = timer()
            tmp_rule = copy.deepcopy(i)
            tmp_rules = copy.deepcopy(rules)
            # se la lughezza della regola è minore di due posso andare a eliminare direttamente l'elemento
            if len(tmp_rule) <= 2:
                tmp_rules.remove(tmp_rules[idx_rule])
                # altrimenti
            else:
                tmp_rule.remove(index)  # rimuove elemento da regola
                tmp_rules[idx_rule] = tmp_rule  # modifico la regola nella lista delle regole

                # Elimino le regole duplicate
                prec_index = None
                for y in tmp_rules[::-1]:
                    if y == tmp_rules[idx_rule]:
                        if prec_index is not None:
                            tmp_rules.remove(tmp_rules[prec_index])
                        prec_index = tmp_rules.index(y)
             # calcolo l'accuracy dopo aver eliminato l'elemento dalla regola
            accuracy = Utilities.allrule_accuracy(tmp_rules, prune_set)
            # mi salvo l'indice della regola, indice dell'elemento e la accuracy ottenuta
            # mi serviranno per poi successivamente scegliere il  migliore
            list_tmp_values.append([idx_rule, index, accuracy])
            end1 = timer()
            print('il tempo impiegato per guardare una  rule è', end1 - start1)
    end = timer()
    print('il tempo impiegato per guardare tutte le rule è', end-start)
    # Trovo potatura che porta a maggiore accuratezza
    for i in list_tmp_values:
        if max_accuracy <= i[2]:
            best_prune = i
            #print(' la regola potata è ',i[1])
            #print(tmp_rules[idx_rule][i[1]])
            max_accuracy = i[2]
            improved = True

    tmp_rules = copy.deepcopy(rules)

    # Apporto la modifica alla regola
    if improved:
        if len(tmp_rules[best_prune[0]]) > 2:
            a = tmp_rules[best_prune[0]].remove(best_prune[1])
            # Cerco duplicati in lista e lascio quello piu' in alto
            print('la regola potata è:',a)
            prec_index = None
            for y in tmp_rules[::-1]:
                if y == tmp_rules[best_prune[0]]:
                    if prec_index is not None:
                        tmp_rules.remove(tmp_rules[prec_index])
                    prec_index = tmp_rules.index(y)
        else:
            tmp_rules.remove(tmp_rules[best_prune[0]])
    else:  # non ho trovato nessun miglioramento
        print("Nessun miglioramento")

    return tmp_rules, max_accuracy, improved

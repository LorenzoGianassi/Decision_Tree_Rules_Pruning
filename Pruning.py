from Utility import *
from timeit import default_timer as timer


# METODO CHE ESGUE LE POTATURE
def pruning(rules, validation_df, training_df):
    improved = True
    count = 0
    start = timer()
    old_original = make_predictions_rule(validation_df, rules)
    new_accuracy = old_original
    while improved:
        count += 1
        print(count)
        rules, new_accuracy, improved = prune_rule(validation_df, rules, new_accuracy)
        print(new_accuracy)
        # se la accuracy sul validation è maggiore o ugaule di quella sul traim mi stoppo
        accuracy_train_df = make_predictions_rule(training_df, rules)
        if new_accuracy >= accuracy_train_df:
            improved = False
    end = timer()
    print("# DI POTATURE:", count-1)
    print("TEMPO DI ESECUZIONE:", (end - start))
    return old_original, rules, new_accuracy


# METODO CHE TROVA LA MIGLIORE POTATURA DA FARE E LA ESEGUE
def prune_rule(df, rules, accuracy):
    copy_rules = copy.deepcopy(rules)
    prune_values = []
    improved = False
    best_accuracy = accuracy
    for index_rule in range(0, len(rules)):
        current_rule = rules[index_rule]
        # ciclo su tutti gli elementi e provo a potarne uno alla volta
        for index_element in range(0, len(current_rule) - 1):
            copy_rule = copy.deepcopy(current_rule)
            copy_rules = copy.deepcopy(rules)
            if len(copy_rule) > 2:
                copy_rule.pop(index_element)
                # rimuovo elemento da regola e sostituisco la regola nella lista delle regole
                copy_rules[index_rule] = copy_rule
                copy_rules = np.unique(copy_rules)
            accuracy = make_predictions_rule(df, copy_rules)
            prune_values.append([index_rule, index_element, accuracy])
    # Trovo potatura che porta a maggiore accuratezza, creando un dataframe per fare argmax della colonna
    prune_values = pd.DataFrame(prune_values, columns=["index_rule", "index_element", "accuracy"])
    max = prune_values.accuracy.argmax()
    best_prune = prune_values.iloc[max]
    if best_prune[2] > best_accuracy:
        best_prune = prune_values.iloc[max]
        best_accuracy = best_prune[2]
        improved = True
    copy_rules = copy.deepcopy(rules)
    # Apporto la modifica alla regola
    if improved:
        copy_rules[int(best_prune[0])].pop(int(best_prune[1]))
        # elimino duplicati
        copy_rules = np.unique(copy_rules)
    else:  # non ho trovato nessun miglioramento
        print("NESSUN MIGLIORAMENTO")

    end = timer()
    return copy_rules, best_accuracy, improved

import numpy as np
import pandas as pd
import copy


# METODO PER PREVEDERE UN ESMPIO UTILIZZANDO DIRETTAMNETE L'ALBERO (DIZIONARIO)
def predict_example(example, tree):
    if not isinstance(tree, dict):
        return tree
    length = len(list(tree.keys()))
    ans_none = False
    for i in range(0, length):
        question = list(tree.keys())[i]
        feature_name, comparison_operator, value = question.split(" ")
        if comparison_operator == "<=":
            if example[feature_name] <= float(value):
                answer = tree[question]
                ans_none = True

        elif comparison_operator == ">":
            if example[feature_name] > float(value):
                answer = tree[question]
                ans_none = True

        # Categorico
        else:
            if str(example[feature_name]) == value:
                ans_none = True
                answer = tree[question]

    if not ans_none:
        answer = np.nan
    if not isinstance(answer, dict):
        return answer
    else:
        residual_tree = answer
        return predict_example(example, residual_tree)


# METODO CHE MI CALCOLA PREDICT EXAMPLE PER OGNI EXAMPLE DEL DATAFRAME
def make_predictions(df, tree):
    if len(df) != 0:
        predictions = df.apply(predict_example, args=(tree,), axis=1)
    else:
        predictions = pd.Series()
    return predictions


# METODO CHE MI CALCOLA L'AACURACY DATA LA SERIE CALCOLATA CON MAKE_PREDICTIONS
def calculate_accuracy(df, tree):
    predictions = make_predictions(df, tree)
    predictions.fillna('non disponibile')
    predictions_correct = predictions == df.income
    accuracy = predictions_correct.mean()
    # avendo un pd che ha come valori tutti booleani considera true e false
    # come 0,1 quindi farne la media corrisponde a trovare la percentuale di valori
    return accuracy


# NUOVO METODO DEL CALCOLO DELLE RULE
def predict_rule(df, rule):
    df_tmp = df
    label = rule[len(rule) - 1]
    df_tmp = df_tmp[df_tmp['income'] == label]
    for index in range(0, len(rule) - 1):
        element = rule[index]
        feature_name, comparison_operator, value = element.split(" ")

        if comparison_operator == "<=":
            df_tmp = df_tmp[df_tmp[feature_name] <= float(value)]
        if comparison_operator == ">":
            df_tmp = df_tmp[df_tmp[feature_name] > float(value)]
            # attributo categorico
        if comparison_operator == "=":
            df_tmp = df_tmp[df_tmp[feature_name] == str(value)]
    index = df_tmp.index
    return index


# METODO PER CALCOLARE ACCURACY PER TUTTE LE RULES
def make_predictions_rule(df, rules):
    total_index = None
    df_tmp = copy.deepcopy(df)
    for i in range(0, len(rules)):
        index = predict_rule(df_tmp, rules[i])
        if total_index is not None:
            total_index = np.concatenate((total_index, index), axis=0)
        else:
            total_index = index
    # utilizzo gli indici, velocizzando l'operazione
    total_index = np.unique(total_index)
    accuracy = (len(total_index)) / df.shape[0]
    return accuracy


# METODO PER CALCOLARE IL NUMERO DI LETTERALI
def number_of_literals(rules):
    count = 0
    for r in rules:
        count += len(r)
    print('Numero di letterali: ', count)

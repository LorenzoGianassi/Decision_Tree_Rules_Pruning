import numpy as np
import copy


# METODO CHE RITORNA TRUE O FALSE SE TUTTI GLI ESEMPI DEL DATAFRAME HANNO LA STESSA CLASSE
def all_same_class(data):
    target_column = data[:, -1]  # ritorna un array di tutti i target realtivi alle righe del dataframe
    classes = np.unique(target_column)  # classi del dataframe
    if len(classes) == 1:  # check se la lista dei target con unique è uguale a 1 ==>  tutti lo stesso tipo di target
        return True
    else:
        return False


# METODO CHE RITORNA LA CLASSE CHE SI TROVA MAGGIORMENTE
def classify_data(data):  # ritorna il valore più popolare di target
    target_column = data[:, -1]
    classes, counts_classes = np.unique(target_column, return_counts=True)
    # ritorna un array con due liste con valori delle classi e il numero delle loro occorrenze
    index = counts_classes.argmax()  # trovo il valore massimo
    classification = classes[index]
    return classification


# CREA UN DIZIONARIO CON CHIAVE ATTRIBUTO E VALORE TUTTI I VALORI CHE ASSUME
def get_values_per_attributes(data):  # per ogni attributo ritorna la lista di valori che può assumere

    potential_splits = {}
    _, n_columns = data.shape
    for column_index in range(n_columns - 1):  # si esclude l'ultima colonna che è la label
        values = data[:, column_index]
        unique_values = np.unique(values)
        potential_splits[column_index] = unique_values
    return potential_splits


# METODO CHE SPLITTA IL DATAFRAME
def split_data(data, split_column, split_value):
    split_column_values = data[:, split_column]

    type_of_feature = FEATURE_TYPES[split_column]
    if type_of_feature == "continuous":
        data_below = data[split_column_values <= split_value]
        data_above = data[split_column_values > split_value]

    # attributo categorico
    else:
        data_below = data[split_column_values == split_value]
        data_above = data[split_column_values != split_value]
    return data_below, data_above


# METODO CHE DETERMINA LA TIPOLOGIA DI ATTRIBUTO
def determine_type_of_attribute(df):
    feature_types = []
    n_unique_values_treshold = 2
    for feature in df.columns:
        if feature != "label":
            unique_values = df[feature].unique()
            example_value = unique_values[0]
            if (isinstance(example_value, str)) or (len(unique_values) <= n_unique_values_treshold):
                feature_types.append("categorical")
            else:
                feature_types.append("continuous")
    # riotrna lista con tipologia di attributo
    return feature_types


# CALCOLA ENTROPIA GENRALE
def calculate_entropy(data):
    target_column = data[:, -1]
    _, counts = np.unique(target_column, return_counts=True)

    probabilities = counts / counts.sum()
    entropy = sum(probabilities * -np.log2(probabilities))
    return entropy


# CALCOLA ENTROPIA DI UN ATTRIBUTO  CONTINUO
def calculate_overall_entropy_continous(data_below, data_above):
    n = len(data_below) + len(data_above)
    p_data_below = len(data_below) / n  # probabilià di dato valido
    p_data_above = len(data_above) / n  # probabilià dato non valido

    overall_entropy = (p_data_below * calculate_entropy(data_below)
                       + p_data_above * calculate_entropy(data_above))
    return overall_entropy


# METODO CHE CALCOLA ENTROPIA DI UN ATTIBUTO CATEGORICO
def calculate_overall_entropy_categorical(data_below, data_above):
    n = len(data_below) + len(data_above)
    p_data_below = len(data_below) / n  # probabilià di dato valido
    # essendo categorico utilizzo solo quello below cioè uguale a valore che assume l'attributo nel sottoalbero
    # non è infatti uno split binario, splitta su ogni valore che può assumere
    overall_entropy = (p_data_below * calculate_entropy(data_below))
    return overall_entropy


# METODO CHE RITORNA VALORE CHE MIFORNISCE MAGGIORE GUADAGNO DI INFORMAZIONE BASATO SULL'ENTROPIA
def determine_best_split(data, values_per_attributes, attributes_value):
    data_entropy = calculate_entropy(data)  # entropia di tutto il sistema
    overall_entropy = 0  # entropia iniziale
    types = FEATURE_TYPES
    for column_index in attributes_value:
        if COLUMN_HEADERS[column_index] != 'fnlwgt':
            if types[column_index] == 'continuous':
                for value in values_per_attributes[column_index]:  # per ogni valore possibile calcoliamo l'entropia
                    data_below, data_above = split_data(data, split_column=column_index, split_value=value)
                    continuos_entropy = calculate_overall_entropy_continous(data_below, data_above)
                    info_gain = data_entropy - continuos_entropy
                    if info_gain >= overall_entropy:
                        overall_entropy = info_gain
                        best_split_column = column_index
                        best_split_value = value
            else:
                categorical_entropy = 0
                for value in values_per_attributes[column_index]:  # per ogni valore possibile calcoliamo l'entropia
                    data_below, data_above = split_data(data, split_column=column_index, split_value=value)
                    categorical_entropy += calculate_overall_entropy_categorical(data_below, data_above)
                info_gain = data_entropy - categorical_entropy
                if info_gain >= overall_entropy:
                    overall_entropy = info_gain
                    best_split_column = column_index
                    best_split_value = value

        else:  # caso in cui l'indice sia due cioè il caso in cui abbia troppi valori, utilizzerò il valore mediano
            data_below, data_above = split_data(data, split_column=column_index,
                                                split_value=np.mean(values_per_attributes[column_index]))
            continuos_entropy = calculate_overall_entropy_continous(data_below, data_above)
            info_gain = data_entropy - continuos_entropy
            if info_gain >= overall_entropy:
                overall_entropy = info_gain
                best_split_column = column_index
                best_split_value = np.mean(values_per_attributes[column_index])
    return best_split_column, best_split_value

    ##############################################################################################################


# ALGORITMO DI APPRENDIMENTO DELL'ALBERO
def decision_tree_algorithm(df, attributes_value=None, counter=0, min_samples=2, max_depth=5):
    # preparazione dati
    # tutti i metodi helper lavorano con numpy e restituiscono numpy.array
    # qundi alla prima iterazione passo df e verrà trasformato in numpy.array
    # alle chimate successive abbiamo un array di numpy come df
    if counter == 0:
        global COLUMN_HEADERS, FEATURE_TYPES
        COLUMN_HEADERS = df.columns
        FEATURE_TYPES = determine_type_of_attribute(df)
        data = df.values
        attributes_value = get_values_per_attributes(df.values)
    else:
        data = df

    if (all_same_class(data)) or (len(data) < min_samples) or (counter == max_depth) or len(attributes_value) == 0:
        classification = classify_data(data)
        return classification

    else:
        counter += 1
        potential_splits = get_values_per_attributes(data)
        # tutti i valori da splittare e si differenziano in categorici o continui
        # nel caso di attributo categorico split_value non lo userò
        split_column, split_value = determine_best_split(data, potential_splits, attributes_value)
        # passo tutti i valori che può assumere i miei attributi e df.values
        if split_column is None or split_value is None:
            classification = classify_data(data)
            return classification

        feature_name = COLUMN_HEADERS[split_column]
        type_of_feature = FEATURE_TYPES[split_column]
        tmp_attributes_value = copy.deepcopy(attributes_value)
        del tmp_attributes_value[split_column]

        sub_tree = {}
        # ATTRIBUTO CONTINUO
        if type_of_feature == "continuous":
            data_below, data_above = split_data(data, split_column, split_value)
            if len(data_below) == 0 or len(data_above) == 0:
                classification = classify_data(data)
                return classification
            question1 = "{} <= {}".format(feature_name, split_value)
            question2 = "{} > {}".format(feature_name, split_value)
            yes_answer = decision_tree_algorithm(data_below, tmp_attributes_value, counter, min_samples, max_depth)
            no_answer = decision_tree_algorithm(data_above, tmp_attributes_value, counter, min_samples, max_depth)
            sub_tree[question1] = yes_answer
            sub_tree[question2] = no_answer
        # ATTRIBUTO CATEGORICO
        else:
            # per ogni valore dell'attributo a questo punto creo una question e otterrò
            for value in potential_splits[split_column]:
                questions = []
                question = "{} = {}".format(feature_name, value)
                questions.append(question)
                # uso il value nel ciclo for
                data_below, _ = split_data(data, split_column, value)
                if len(data_below) == 0:
                    classification = classify_data(data)
                    return classification
                answer = decision_tree_algorithm(data_below, tmp_attributes_value, counter, min_samples, max_depth)
                sub_tree[question] = answer
        return sub_tree

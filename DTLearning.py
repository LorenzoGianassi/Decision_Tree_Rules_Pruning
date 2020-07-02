import DT
import math
import DataSet


def dt_learner(dataset):

    # funzione che classifica se un esempio ha un valore dell'attribute maggiore o minore  della treshold
    # calcolata al relativo attribute che gli viene passata
    def treshold_classifier(examples, attribute, value):
        exs_val = []
        exs_non_val = []
        if attribute in dataset.cont:
            for e in examples:
                if float(e[attribute]) <= value:
                    exs_val.append(e)
                else:
                    exs_non_val.append(e)
        else:
            for e in examples:
                if e[attribute] == value:
                    exs_val.append(e)
                else:
                    exs_non_val.append(e)
        return exs_val, exs_non_val

    # funzione che calcola il numero di examples con valore uguale a value per l'attribute passato
    def counting(attribute, value, example):
        return sum(e[attribute] == value for e in example)

    # funzione che elimina l'attributo che è stato appena messo nel tree

    def update_attributes(delAttr, attributes):
        result = list(attributes)
        result.remove(delAttr)
        return result

    def information_gain1( attribute, examples):
        entr = entropy(examples)
        gain = 0
        threshold = 0
        for v in DataSet.values(attribute, dataset.examples):
            tmp_rem = remainder(attribute, v, examples)
            tmp_gain = entr - tmp_rem
            if tmp_gain > gain:
                gain = tmp_gain
                threshold = v
        return gain, threshold

    def information_gain2(attribute, examples):
        entr = entropy(examples)
        rem = remainder2(attribute, examples)
        gain = entr - rem  # Gain(Decision, X) = Entropy(Decision) – ∑ [ p(Decision|X) * Entropy(Decision|X) ]
        val = DataSet.values(attribute, dataset.examples)
        return gain, val

    def remainder(attribute, value, examples):  # calcola il valore ∑ [ p(Decision|X) * Entropy(Decision|X) ]
        tot = float(len(examples))
        over_treshold, under_treshold = treshold_classifier(examples, attribute, value)
        remainder_over = (float(len(over_treshold)) / tot) * entropy(over_treshold)
        remainder_under = (float(len(under_treshold)) / tot) * entropy(under_treshold)
        rem = remainder_over + remainder_under
        return rem

    def remainder2(attribute, examples):
        tot = float(len(examples))
        rem = 0
        for v in DataSet.values(attribute, examples):
            val, non_val = treshold_classifier(examples, attribute, v)
            remainder_val = (float(len(val)) / tot) * entropy(val)  # entropia associata al val
            rem += remainder_val
        return rem

    def entropy(examples):  # funzione che calcola entropia
        entr = 0
        tot = len(examples)
        if tot != 0:
            for v in dataset.values:
                e = float(counting(dataset.target, v, examples)) / tot
                if e != 0:
                    entr += (-e) * math.log(e, 2.0)
        return float(entr)

    def plurality_value(examples):  # funzione che mi calcola il valore del target più popolare
        i = 0
        global popular
        for v in dataset.values:
            cnt = counting(dataset.target, v, examples)
            if cnt > i:
                i = cnt
                popular = v
        return DT.Leaf(popular)

    def check_target_values(examples):
        v = examples[0][dataset.target]
        for e in examples:
            if e[dataset.target] != v:
                return False
        return True

    # trova il piu importante attributo e suo trehshold in accordo all'information gain
    def importance_attr(attributes, examples):
        global mostImportanceAttr
        maxgainAttr = 0
        value = 0
        values = []
        for a in attributes:
            if a in dataset.cont:  # in queso caso avro solamente la threshold
                gain, val1 = information_gain1(a, examples)
                gain = gain
            elif a in dataset.cat:  # in questo caso avrò la lista dei valori che può assumere l'attribute scelto
                gain, val2 = information_gain2(a, examples)
                gain = gain
            if gain >= maxgainAttr:
                mostImportanceAttr = a
                maxgainAttr = gain
                if mostImportanceAttr in dataset.cont:
                    value = val1
                else:
                    values = val2
        if mostImportanceAttr in dataset.cont:
            return mostImportanceAttr, value, maxgainAttr
        else:
            return mostImportanceAttr, values, maxgainAttr

    # funzione che mi attua il learning dell'albero
    def learner(examples, attributes, parents_examples=()):
        if len(examples) == 0:
            return plurality_value(parents_examples)
        elif check_target_values(examples):
            return DT.Leaf(examples[0][dataset.target])
        elif len(attributes) == 0:
            return plurality_value(examples)
        else:
            imp_attr, val, gain = importance_attr(attributes, examples)
            tree = DT.DecisionTree(imp_attr, val, dataset.attribute_names[imp_attr])
            if imp_attr in dataset.cont:
                exs = treshold_classifier(examples, imp_attr, val)
                for v in exs[::-1]:
                    new_attributes = update_attributes(imp_attr, attributes)
                    branch = learner(v, new_attributes, examples)
                    tree.add(val, exs.index(v), branch)
            else:
                for v in val[::-1]:
                    index = val.index(v)
                    new_exs, no_exs = treshold_classifier(examples, imp_attr, v)
                    new_branch = learner(new_exs, update_attributes(imp_attr, attributes), examples)
                    tree.add(v, index, new_branch)
            return tree

    tr = learner(dataset.examples, dataset.inputs)
    print('training finished')
    return tr

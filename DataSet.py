from random import shuffle
import pandas as pd


class DataSet:
    def __init__(self, examples=None, inputs=None, attributes=None, target=None, attribute_names=None, values=None,
                 cat=None, cont=None):
        self.examples = examples
        self.target = target
        self.values = values
        self.inputs = inputs
        self.attributes = attributes
        self.attribute_names = attribute_names or attributes
        self.cat = cat
        self.cont = cont


def parse(file, values):
    data = pd.read_csv(file, sep=',')

    # trovo tutti i valori missing e elimino le rispettive righe
    col_names = data.columns

    data = data[data['workclass'] != '?']
    data = data[data['occupation'] != '?']
    data = data[data['native-country'] != '?']
    data = data.reset_index(drop=True)

    attribute_names = list(data.columns.values)

    target = attribute_names[len(attribute_names) - 1]

    attributes = []
    for i in range(0, len(attribute_names)):
        attributes.append(i)

    target = attributes[len(attribute_names) - 1]
    inputs = list(attributes)
    inputs.pop(attributes.index(target))

    examples = data.values.tolist()
    cont = []
    cat = []
    for a in attributes:
        if isinstance(examples[0][a], int):
            cont.append(a)
        else:
            cat.append(a)

    return DataSet(examples, inputs, attributes, target, attribute_names, values, cat, cont)


def splitting(dataset):
    shuffle(dataset.examples)  # per non dipendere da una una precisa configurazione del dataset
    train_validation_length = int((len(dataset.examples) * 2) / 3)
    # faccio i due terzi del totale che saranno a sua volta divisi
    training_length = int((train_validation_length * 2) / 3)
    validation_length = train_validation_length - training_length
    test_length = int(len(dataset.examples) - train_validation_length)

    training_examples = []
    validation_examples = []
    test_examples = []

    for e in range(0, training_length):
        training_examples.append(dataset.examples[e])

    for e in range(training_length, training_length + validation_length):
        validation_examples.append(dataset.examples[e])

    for e in range(training_length + validation_length, training_length + validation_length + test_length):
        test_examples.append(dataset.examples[e])

    training = DataSet(training_examples, dataset.inputs, dataset.attributes,
                       dataset.target, dataset.attribute_names, dataset.values, dataset.cat, dataset.cont)

    validation = DataSet(validation_examples, dataset.inputs, dataset.attributes,
                         dataset.target, dataset.attribute_names, dataset.values, dataset.cat, dataset.cont)

    test = DataSet(test_examples, dataset.inputs, dataset.attributes,
                   dataset.target, dataset.attribute_names, dataset.values, dataset.cat, dataset.cont)

    return training, validation, test


# metodo che ritorna tutti i valori che può assumere una attributo
def values(attribute, examples):
    val = []
    for i in examples:
        if not i[attribute] in val:
            val.append(i[attribute])
    return val

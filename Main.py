from Rules import *
from DataSet import *
from Learning import *
from Pruning import *
import matplotlib.pyplot as plt

# CREAZIONE DI TRAIN-SET, VALIDATION-SET E TEST-SET
df = create_dataframe()
dim_df = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]

# METODO CHE FA IL PLOT DELLE PRECISIONI DELLE VARIE DEPTH DELL'ALBERO
def plot_depth():
    y = [[], [], []]
    x = []
    for i in range(3, 15):
        tree = decision_tree_algorithm(train_df, counter=0, min_samples=2, max_depth=i)
        y[0].append(calculate_accuracy(train_df, tree))
        y[1].append(calculate_accuracy(test_df, tree))
        y[2].append(calculate_accuracy(validation_df, tree))
        x.append(i)

    plt.xlabel('Depth Albero')
    plt.ylabel('Accuracy')
    plt.grid()
    plt.plot(x, y[0])
    plt.plot(x, y[1])
    plt.plot(x, y[2])

    plt.title("Calcolo Accuracy al variare della depth")
    plt.legend(['Train-Set', 'Test-Set', 'Validation-Set'])
    plt.savefig('depth_prova.png', bbox_inches='tight')
    plt.clf()

# METODO CHE FA IL PLOT SECONDO LA DIMENSIONE
def plot_dim(dim):
    y = [[], [], []]
    x = []
    for i in dim:
        indices = df.index.tolist()
        test_indices = random.sample(population=indices, k=i)
        new_df = df.loc[test_indices]
        train_df, test_df = df_split(new_df, 0.20)
        train_df, validation_df = df_split(train_df, 0.20)
        tree = decision_tree_algorithm(train_df, counter=0, min_samples=2, max_depth=8)
        y[0].append(calculate_accuracy(train_df, tree))
        y[1].append(calculate_accuracy(test_df, tree))
        y[2].append(calculate_accuracy(validation_df, tree))
        x.append(i)

    plt.xlabel('Grandezza Dataset')
    plt.ylabel('Accuracy')
    plt.grid()
    plt.plot(x, y[0])
    plt.plot(x, y[1])
    plt.plot(x, y[2])

    plt.title("Calcolo Accuracy al variare della Dimensione del Dataset")
    plt.legend(['Train-Set', 'Test-Set', 'Validation-Set'])
    plt.savefig('dim_prova.png', bbox_inches='tight')
    plt.clf()


# ESECUZIONE DEL PRUNING E PRINT DELLE ACCURACIES PRE E POST PRUNING
def pruning_table():
    accuracy_original, new_rules, accuracy_pruned = pruning(rules, validation_df, train_df)
    y = []
    y.append(calculate_accuracy(train_df, tree))
    y.append(calculate_accuracy(validation_df, tree))
    y.append(calculate_accuracy(test_df, tree))
    y.append(make_predictions_rule(train_df, new_rules))
    y.append(make_predictions_rule(validation_df, new_rules))
    y.append(make_predictions_rule(test_df, new_rules))

    legend = ['Train-Set', 'Validation-Set', 'Test-Set']
    for i in range(0, 3):
        print('{}'.format(i), ' & ', '{}'.format(int(y[i] * 100)), '%', ' & ',
              '{}'.format(int(y[i + 3] * 100)), '%')
    print("----------------------------------------------------")
    plt.ylim(0, 1)
    plt.bar([0, 1, 2, 4, 5, 6], y,
            tick_label=["Training", "Validation", "Test", "Training", "Validation", "Test"])
    plt.title("Accuracy Pre-Post Pruning")
    plt.xlabel("Decision Tree                                      Pruned Tree")
    plt.ylabel("Accuracy")

    plt.savefig("./pruning.png", dpi=72)

    ################################################################################################################
indices = df.index.tolist()
test_indices = random.sample(population=indices, k=8000)
new_df = df.loc[test_indices]
train_df, test_df = df_split(new_df, 0.20)
train_df, validation_df = df_split(train_df, 0.20)
tree = decision_tree_algorithm(train_df, counter=0, min_samples=2, max_depth=8)
rules = all_rules(tree)

print(len(rules), 'numero di regole')
rules = np.array(rules, dtype=object)
number_of_literals(rules)
# richiamo i metodi di plot
plot_depth()
plot_dim(dim_df)
pruning_table()

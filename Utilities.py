import matplotlib.pyplot as plt


def rule_accuracy(rule, dataset):
    correct = []
    verified = True
    for e in dataset.examples:
        for r in rule[:len(rule) - 2]:
            if rule[len(rule) - 1] != e[len(e) - 1]:
                verified = False
                break
            if r[0] in dataset.cont:
                if (r[2] == 0 and r[1] <= e[r[0]]) or (r[2] == 1 and r[1] > e[r[0]]):
                    verified = True
                else:
                    verified = False
                    break
            else:
                if e[r[0]] == r[1]:
                    verified = True
                else:
                    verified = False
                    break
        if verified:
            correct.append(e)
    return correct


def allrule_accuracy(rules, dataset):
    correct = []
    for r in rules:
        corr = rule_accuracy(r, dataset)
        correct.extend(corr)
    corr = []
    len(correct)

    for c in correct:
        if c not in corr:
            corr.append(c)
    exs_correct = len(corr) / len(dataset.examples)
    percent = (len(corr) * 100) / len(dataset.examples)
    """""
    print(percent, '% classificate correttamente, ovvero', len(corr),
           'classificazioni corrette su', len(dataset.examples))
    """
    return percent, exs_correct


def graph(values):
    plt.ylim(0, 100)
    plt.bar([0, 1, 2, 4, 5, 6], values,
            tick_label=["Training", "Validation", "Test", "Training", "Validation", "Test"])
    plt.title("Accuracy Pre-Pruning  Post-Pruning")
    plt.ylabel("Accuracy")
    plt.xlabel("Decision Tree                                               Pruned Tree")
    plt.show()
    return

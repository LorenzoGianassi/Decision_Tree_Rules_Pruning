import DataSet
import DTLearning
import Pruning
import Utilities
file = 'adult_2000.csv'
file_Class_values = ['<=50K', '>50K']
dataset = DataSet.parse(file, file_Class_values)

numtest = 1
tmp_exs1 = 0
tmp_exs2 = 0
tmp_exs3 = 0
pr_tmp_exs1 = 0
pr_tmp_exs2 = 0
pr_tmp_exs3 = 0
for i in range(0, numtest):
    training, validation, test = DataSet.splitting(dataset)
    tree = DTLearning.dt_learner(training)
    dnf_tree = Pruning.all_rules(tree)
    #for i in dnf_tree:
    #    print(i)
    correct1, exs_corr1 = Utilities.allrule_accuracy(dnf_tree, test)
    correct2, exs_corr2 = Utilities.allrule_accuracy(dnf_tree, validation)
    correct3, exs_corr3 = Utilities.allrule_accuracy(dnf_tree, training)
    corr, new_rules, new_correct = Pruning.pruning(dnf_tree, validation, training)
    #for i in new_rules:
    #   print(i)
    pr_correct1, pr_exs_corr1 = Utilities.allrule_accuracy(new_rules, test)
    pr_correct2, pr_exs_corr2 = Utilities.allrule_accuracy(new_rules, validation)
    pr_correct3, pr_exs_corr3 = Utilities.allrule_accuracy(new_rules, training)

    tmp_exs1 += exs_corr1
    tmp_exs2 += exs_corr2
    tmp_exs3 += exs_corr3

    pr_tmp_exs1 += pr_exs_corr1
    pr_tmp_exs2 += pr_exs_corr2
    pr_tmp_exs3 += pr_exs_corr3


tmp_exs1 = (tmp_exs1/numtest)*100
tmp_exs2 = (tmp_exs2/numtest)*100
tmp_exs3 = (tmp_exs3/numtest)*100

pr_tmp_exs1 = (pr_tmp_exs1/numtest)*100
pr_tmp_exs2 = (pr_tmp_exs2/numtest)*100
pr_tmp_exs3 = (pr_tmp_exs3/numtest)*100
print('Accuracy Pre-Pruning')
print('training', tmp_exs3, '%', 'test', tmp_exs1, '%',  'validation', tmp_exs2, '%')
print('Accuracy Post-Pruning')
print('training', pr_tmp_exs3, '%', 'test', pr_tmp_exs1, '%',  'validation', pr_tmp_exs2, '%')

#accuracies = [tmp_exs3, tmp_exs2, tmp_exs1, pr_tmp_exs3, pr_tmp_exs2, pr_tmp_exs1]
#Utilities.graph(accuracies)

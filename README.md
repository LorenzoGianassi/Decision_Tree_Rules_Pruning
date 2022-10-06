# Decision Tree Rules Pruning
## Table of Contents  
- [About the Project](#1)  
- [Dataset](#2)  
- [Usage](#4)
# About the Project <a name="1"/>
The purpose of the project is to create a decision tree using the ID3 algorithm with entropy impurity measurement. Once the decision tree has been created, the Pruning strategy will be implemented, so it will be necessary to transform the tree into rules that represent all the paths from roots to leaves. The Pruning strategy will be performed by evaluating the error on the ValidationSet. Finally, we will go to perform the comparisons on the accuracy before and after the operation
by Pruning.
# Dataset <a name="2"/>
In this project, we will use a standard imbalanced machine learning dataset referred to as the “Adult Income” or simply the “adult” dataset.

The dataset is credited to Ronny Kohavi and Barry Becker and was drawn from the 1994 United States Census Bureau data and involves using personal details such as education level to predict whether an individual will earn more or less than $50,000 per year.

The dataset contains 16 columns.

Target filed: Income
- The income is divide into two classes: <=50K and >50K <br>

Number of attributes: 14
- These are the demographics and other features to describe a person

We can explore the possibility in predicting income level based on the individual’s personal information.
# Usage <a name="4"/>

- Download and save a .csv file in the Project folder, in particular the DatasSet.py file will deal specifically with the dataset used so changes to the code in that class will be necessary in case you want to use another dataset.
In the .csv file, the first line must contain the names of the dataset attributes. For the dataset parse I used Pandas, so you will need to download it too.
- In the Main.py file we will run more tests in order to analyze the problem more in depth. In particular, how the accuracy varies depending on the depth of the tree and the number of examples that are used to create and test the tree.

Execution times may vary depending on the size of the dataset and the depth of the tree (the pruning operation is the one that takes the most time).

For the realization of this project I have consulted the following sources:
- Two public repositories adapted to my problem: https://github.com/aimacode/aima-python/blob/master/learning.py, https://github.com/SebastianMantey/Decision-Tree-from-Scratch/tree/master/notebooks
- The paragraph of the book provided by the problem request: 'Machine Learning', Tom M. Mitchell (1997), McGraw-Hill
- Textbook: 'Artificial Intelligence: A Modern Approach', by Stuart J. Russell and Peter Norvig


# Authors
- **Lorenzo Gianassi**
# Acknowledgments
Parallel Computing Project © Course held by Professor [Marco Bertini](https://www.unifi.it/p-doc2-2019-0-A-2b333d2d3529-1.html) - Computer Engineering Master Degree @[University of Florence](https://www.unifi.it/changelang-eng.html)


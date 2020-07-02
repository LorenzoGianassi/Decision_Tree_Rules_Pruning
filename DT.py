class DecisionTree:

    def __init__(self, attribute, threshold, attribute_name=None, branches=None, branch_number=None):
        self.attr = attribute
        self.threshold = threshold
        self.attribute_name = attribute_name or attribute
        self.branches = branches or {}
        self.branch_number = branch_number

    def add(self, value, index, subtree):
        self.branches[(self.attribute_name, value, index)] = subtree

    def get(self, value, index):
        tree = self.branches.get((self.attribute_name, value, index))
        return tree


class Leaf:
    def __init__(self, result):
        self.result = result

    def __call__(self, example):
        return self.result


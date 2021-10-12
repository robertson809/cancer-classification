from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle
from sklearn import preprocessing
from sklearn.feature_selection import VarianceThreshold
import pandas
import time
import numpy as np


def find_f_1(predicted, actual):
    """
    Returns f_1 metrics, hardcoded specific to the MNIST 1 to ten classification
    :param predicted: list of string integers
    :param actual: list of string integers
    :return: f_1_dict dictionary of the f_1 scores for each number
    """
    f_1_dict = {}
    for i in range(6):
        correct_positive = 0
        predicted_positive = 0
        total_positive = 0
        for j in range(predicted.size):
            if predicted[j] == i:
                predicted_positive += 1
                if actual[j] == i:
                    correct_positive += 1
                    total_positive += 1
            elif actual[j] == i:
                total_positive += 1
        precision = correct_positive / predicted_positive
        recall = correct_positive / total_positive
        f_1_dict[i] = 2 * (precision * recall) / (precision + recall)
    return f_1_dict


def split(data):
    """
    returns a train, validate, and test dictionary
    """
    split_dict = {}
    split_dict.update({'train': data[0:int(len(data) * 0.8)]})
    split_dict.update({'validate': data[int(len(data) * 0.8):int(len(data) * 0.95)]})
    split_dict.update({'test': data[int(len(data) * 0.95)::]})
    return split_dict


print("Reading csvs")
features = pandas.read_csv('../data/Cleaned/features.csv')
print('Feature size is', features.size)
#print('features are \n', features)
#print('feature 1', features.head())

targets = np.genfromtxt('../data/Cleaned/targets.csv', dtype=str, delimiter=',').tolist()
for i in range(len(targets)): #remove extra shit
    targets[i] = int(targets[i].strip('\'\"'))

# shuffle the data to ensure that we're testing on all possible targets
features, targets = shuffle(features, targets, random_state=0)

#scaling
features_scaled = preprocessing.scale(features)
# print(len(features_scaled), 'features before feature selection')
sel = VarianceThreshold()
features_scaled = sel.fit_transform(features_scaled)
# print(len(features_scaled), 'features after fs')


#print(features_scaled)
features_dict = split(features_scaled)
targets_dict = split(targets)

#targets_columns = targets_dict['train'].columns
classifier1 = DecisionTreeClassifier(criterion = "entropy", max_depth = 100)
classifier2 = LogisticRegression(solver = 'liblinear', multi_class= 'auto')

print("Fitting Models")
start = time.time()

classifier1 = classifier1.fit(features_dict['train'], targets_dict['train'])
classifier2 = classifier2.fit(features_dict['train'], targets_dict['train'])

print("Done in {0:03.2f} seconds".format((time.time()-start)/60))

# make predictions for all of the validation data
clf1_predictions = classifier1.predict(features_dict['validate'])
clf2_predictions = classifier2.predict(features_dict['validate'])

f_1_dict = find_f_1(clf1_predictions, targets_dict['validate'])
print('f1 scores for our cancers with Decision Tree are')
for number in list(f_1_dict.values()):
    print('{:.2f} & '.format(number), end='')
print('\n')
f_1_dict = find_f_1(clf2_predictions, targets_dict['validate'])
print('f1 scores for our cancers with Logistic Regression are')
for number in list(f_1_dict.values()):
    print('{:.2f} & '.format(number), end='')
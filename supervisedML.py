"""
supervisedML.py - Supervised Machine Learning Model Trainer

This script is designed to train multiple classifiers on a dataset and select the best-performing one.
The training function reads a CSV dataset, splits it into training and testing sets, and then iterates through various
classifier configurations.
For each configuration, it measures training and testing durations, computes accuracy, and prints the results.
After evaluating all classifiers, it identifies the best-performing model and saves it using pickle.
"""
import os
import pickle

import pandas
import sklearn
from sklearn import tree
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import VotingClassifier, StackingClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

from util import current_ms, getDestinationFolder, unchangingColumns


def training():
    my_df = pandas.read_csv(getDestinationFolder() + "dataset.csv", sep=',')

    y = my_df["label"]
    x = my_df.drop(columns=["timestamp", "label"] + (unchangingColumns()))  # filter the dataset excluding the columns with less variation

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, shuffle=False)  # splitting the dataset

    classifiers = [VotingClassifier(estimators=[('lda', LinearDiscriminantAnalysis()),
                                                ('nb', GaussianNB()),
                                                ('dt', tree.DecisionTreeClassifier())]),
                   VotingClassifier(estimators=[('lda', LinearDiscriminantAnalysis()),
                                                ('nb', GaussianNB()),
                                                ('rf', RandomForestClassifier(n_estimators=20))]),
                   StackingClassifier(estimators=[('lda', LinearDiscriminantAnalysis()),
                                                  ('nb', GaussianNB()),
                                                  ('dt', tree.DecisionTreeClassifier())],
                                      final_estimator=RandomForestClassifier(n_estimators=10)),
                   StackingClassifier(estimators=[('lda', LinearDiscriminantAnalysis()),
                                                  ('nb', GaussianNB()),
                                                  ('dt', tree.DecisionTreeClassifier())],
                                      final_estimator=KNeighborsClassifier(n_neighbors=11)),
                   tree.DecisionTreeClassifier(), GaussianNB(),
                   LinearDiscriminantAnalysis(), KNeighborsClassifier(n_neighbors=11),
                   KNeighborsClassifier(n_neighbors=25), RandomForestClassifier(n_estimators=10),
                   RandomForestClassifier(n_estimators=3), RandomForestClassifier(n_estimators=20)]
    clf_results = []
    for i, clf in enumerate(classifiers):
        start_time_training = current_ms()
        clf = clf.fit(x_train, y_train)
        end_time_training = current_ms()
        predicted_labels = clf.predict(x_test)
        end_time = current_ms()
        accuracy = sklearn.metrics.accuracy_score(y_test, predicted_labels)
        print(f"Classifier: {classifiers[i]}, Accuracy: {accuracy}, "
              f"Training duration: {end_time_training - start_time_training}, Testing duration: {end_time - end_time_training}")
        clf_results.append({
            'classifier': classifiers[i],
            'accuracy': accuracy,
            'training_duration': end_time_training - start_time_training,
            'testing_duration': end_time - end_time_training
        })
    model = findBest(clf_results)
    clf_model = model['classifier'].fit(x_train, y_train)
    if not os.path.exists("anomaly_detector"):
        os.makedirs("anomaly_detector")
    with open('anomaly_detector/anomaly_detector_model.pkl', 'wb') as model_file:
        pickle.dump(clf_model, model_file)
    return clf_results


def findBest(results):
    best = {'classifier': "", 'accuracy': 0}
    for r in results:
        if r['accuracy'] > best['accuracy']:
            best['accuracy'] = r['accuracy']
            best['classifier'] = r['classifier']
    print("The best classifier is: ", best['classifier'], "with accuracy: ", best['accuracy'])
    return best


if __name__ == "__main__":
    training()

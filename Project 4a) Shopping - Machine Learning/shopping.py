import csv
import sys
import random

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def data_formating(data):
    new_data = []
    integers = ["Administrative", "Informational", "ProductRelated", "OperatingSystems", "Browser", "Region", "TrafficType"]
    month_to_int = {"Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5, "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11}
    for row in data:
        new_evidence = []
        for evidence, value in row["evidence"].items():
            if evidence == "Month":
                new_evidence.append(month_to_int[value])
            elif evidence == "VisitorType" or evidence == "Weekend":
                if value == "Returning_Visitor" or value == "TRUE":
                    new_evidence.append(int(1))
                else:
                    new_evidence.append(int(0))
            elif evidence in integers:
                new_evidence.append(int(value))
            else:
                new_evidence.append(float(value))
        new_data.append({"evidence": new_evidence, "label": row["label"]})
    return new_data

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        headers  = next(reader)
        data = []
        for row in reader:
            evidence = dict(zip(headers[:-1], row[:-1]))
            data.append({'evidence': evidence, 'label': 1 if row[-1] == "TRUE" else 0})

    data = data_formating(data)
    return ([row["evidence"] for row in data], [row["label"] for row in data])


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    return model.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    tp, tn, fp, fn = 0, 0, 0, 0    
    for actual, prediction in zip(labels, predictions):
        if prediction == 1 and actual == 1: tp += 1
        if prediction == 0 and actual == 0: tn += 1
        if prediction == 1 and actual == 0: fp += 1
        if prediction == 0 and actual == 1: fn += 1
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    return (sensitivity, specificity)

if __name__ == "__main__":
    main()

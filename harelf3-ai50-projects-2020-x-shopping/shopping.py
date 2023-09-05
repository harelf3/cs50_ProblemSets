import csv
import sys

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
    evidence = []
    labels = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        # skipping first line 
        next(reader)
        for row in reader:
            evidence_tmp= []
            labels_tmp = 0
             # we got 18 iterations 
            parameter_list = row[0].split(",")
            parameter_list_len = len(parameter_list)
            for parameter in range(parameter_list_len):
                if parameter in {0,2,4,11,12,13,14}:
                    evidence_tmp.append(int(parameter_list[parameter]))
                    continue
                if parameter in {1,3,5,6,7,8,9}:
                    evidence_tmp.append(float(parameter_list[parameter]))
                    continue
                if parameter == 10 :
                    evidence_tmp.append(int(months.index(parameter_list[parameter])))
                    continue
                if parameter == 15 :
                    if parameter_list[parameter] == "New_Visitor":
                        evidence_tmp.append(0)
                    else :
                        evidence_tmp.append(1)
                    continue
                if parameter ==16:
                    if parameter_list[parameter] == "FALSE":
                        evidence_tmp.append(0)
                    else:
                        evidence_tmp.append(1)
                    continue
                if parameter == 17 :
                    if parameter_list[parameter] == "FALSE":
                        labels_tmp = 0
                    else:
                        labels_tmp = 1
                    continue
                
            evidence.append(evidence_tmp)
            labels.append(labels_tmp)
                    

    return (evidence,labels)    


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    
    """ holdout = int(0.40 * len(evidence))
    evtesting = evidence[:holdout]
    latesting = labels[:holdout]
    evtraining = evidence[holdout:]
    latraining = labels[holdout:] """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model
    
    


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # for sensitivity positives how much/predicted positives predicted positives/ predicted positives 
    # for specificity negatives / predicted negatives 
    positives = 0 
    negatives = 0
    negative_correct = 0
    positive_correct = 0
    for actual, predicted in zip(labels, predictions):
        # negative
        if actual == 0:
            negatives+=1
            if actual == predicted:
                negative_correct+=1
        else:
            positives+=1
            if actual == predicted:
                positive_correct+=1
    sensitivity = positive_correct/positives
    specifity = negative_correct/negatives
    return(sensitivity,specifity)
                
    


if __name__ == "__main__":
    main()

from statModel import getStatistics, convertTestTable
from nb import predict
from knn import knn, read_data


def getFolds():
    folds = []
    yesList = []
    noList = []

    table = getStatistics("../pima.csv")
    for line in table.dataLines:
        if line[-1] == "yes":
            table.yesCount += 1
            yesList.append(line)
        else:
            table.noCount += 1
            noList.append(line)

    for i in range(0, 10):
        folds.append([])

    i = 0
    while(len(yesList) > 0):
        folds[i % 10].append(yesList.pop(0))
        i += 1

    i = 0
    while(len(noList) > 0):
        folds[i % 10].append(noList.pop(0))
        i += 1

    # !!! CODE USED TO GENERATE THE PIMA-FOLDS.CSV FILE
    # with open('pima-folds.csv', 'w') as f:
    #     i = 1
    #     for fold in folds:
    #         f.write("fold" + str(i) + "\n")
    #         for line in fold:
    #             converted_line = [str(element) for element in line]
    #             f.write(",".join(converted_line) + "\n")
    #         f.write("\n")
    #         i += 1
    return folds

def calculate_err(prediction, actual):
    pass

def ten_fold_validation(folds, algorithm):

    testing_path = "fold-testing.csv"
    training_path = "fold-training.csv"

    for i in range(0, 10):
        training = []
        test = []
        actual = []

        # Get the testing set (without the class), the actual class of each line will be written into the 'actual' list
        for line in folds[i]:
            newLine = []
            for attr in line:
                if attr == "yes" or attr == "no":
                    actual.append(attr)
                    break
                newLine.append(attr)
            test.append(newLine)

        # Ignore the testing set, add the rest for training
        for j in range(0, 10):
            if j == i:
                continue
            training.append(folds[j])

        with open('fold-training.csv', 'w') as f:
            for fold in training:
                for line in fold:
                    converted_line = [str(element) for element in line]
                    f.write(",".join(converted_line) + "\n")

        with open('fold-testing.csv', 'w') as f:
            for line in test:
                converted_line = [str(element) for element in line]
                f.write(",".join(converted_line) + "\n")

        if algorithm == "NB":

            predicted = predict(training_path, testing_path)

            error = 0
            for k in range(len(predicted)):
                if(predicted[k] != actual[k]):
                    error += 1
            correct = len(predicted)-error
            print("Result of validation {} is:\nCorrect: {}\nError: {}\nAccuracy Rate: {}\n".format(
                i+1, correct, error, correct/len(predicted)))

        else:
            k = int(algorithm[0])

            testing_data = convertTestTable(testing_path).dataLines
            training_data = read_data(training_path).get_table()
            
            predicted = knn(testing_data, training_data, k)

            error = 0
            for k in range(len(predicted)):
                if(predicted[k] != actual[k]):
                    error += 1
            correct = len(predicted)-error
            print("Result of validation {} is:\nCorrect: {}\nError: {}\nAccuracy Rate: {}\n".format(
                i+1, correct, error, correct/len(predicted)))



# matrixTable = sortTable(trainingTable)
# matrixStat = detailData(matrixTable)
folds = getFolds()

ten_fold_validation(folds, "NB")

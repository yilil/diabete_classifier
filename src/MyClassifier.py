import sys
from nb import predict
from knn import knn, read_data
from statModel import convertTestTable

trainingPath = sys.argv[1]
testingPath = sys.argv[2]
classifer = sys.argv[3]

if classifer == "NB":
    result = predict(trainingPath, testingPath)
    for i in result:
        print(i)
else:
    k = int(classifer[0])
    
    testing_data = convertTestTable(testingPath).dataLines
    training_data = read_data(trainingPath).get_table()

    
    results = knn(testing_data, training_data, k)
    
    for x in results:
        print(x)


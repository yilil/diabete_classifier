import statistics
import math
from statModel import getStatistics, DataModel, convertTestTable

class attrStat:
    def __init__(self):
        self.mean = 0
        self.sd = 0

#sort out table into a 2D matrix, in the form of [[[attr1 class yes][attr1 class no]], [[attr2 class yes][attr2 class no]]...]
def sortTable(table):
    matrixTable = []
    for line in table.dataLines:
        classType = line[-1]
        if classType != "yes" and classType != "no":
            print("Error")
            exit()

        if(classType == "yes"):
            table.yesCount += 1
        else:
            table.noCount += 1

        if(len(matrixTable) == 0):
            for attr in line:
                if attr == classType:
                    break
                yesList = []
                noList = []
                if classType == "yes":
                    yesList.append(attr)
                else:
                    noList.append(attr)
                matrixTable.append([yesList, noList])
        else:
            for i in range(len(line)):
                attr = line[i]
                if line[i] == classType:
                    break
                if classType == "yes":
                    matrixTable[i][0].append(attr)
                else:
                    matrixTable[i][1].append(attr)
    return matrixTable

#Given a sorted matrixtable, find the mean and sd for each attribute of class yes and no
def detailData(matrixTable):
    result = []
    for attr in matrixTable:
        yesStat = None
        noStat = None
        classType = ""
        for i in range(2):
            if i == 0:
                classType = "yes"
            else:
                classType = "no"

            #classList will store all instances/values of a variable of a specific class
            classList = attr[i]
            newStat = attrStat()

            if(len(classList) == 0):
                return "Division by zero! Check classList length!"

            newStat.mean = sum(classList) / len(classList)
            newStat.sd = statistics.stdev(classList)
            if classType == "yes":
                yesStat = newStat
            else:
                noStat = newStat

        result.append([yesStat, noStat])
    return result

#The probability density function
def pDensity(data, dataStat):
    sd = dataStat.sd
    mean = dataStat.mean
    # if(sd == 0):
    #     return 0
        
    factor = (1 / ( sd * math.sqrt(2 * math.pi)))
    exp = math.pow(math.e, -1 * (math.pow(data - mean,2)/(2* math.pow(sd, 2))))
    return factor * exp

def predict(trainingPath, testingPath):
    trainingTable = getStatistics(trainingPath)
    testingTable = convertTestTable(testingPath)
    
    matrixTable = sortTable(trainingTable)
    matrixStat = detailData(matrixTable)
    result = []
    for line in testingTable.dataLines:
        yesP = trainingTable.yesCount/len(trainingTable.dataLines)
        noP = trainingTable.noCount/len(trainingTable.dataLines)

        for i in range(trainingTable.attrCount):
            data = line[i]
            dataStat = matrixStat[i][0]
            yesP *= pDensity(data, dataStat)

        for i in range(trainingTable.attrCount):
            data = line[i]
            dataStat = matrixStat[i][1]
            noP *= pDensity(data, dataStat)
        # print(yesP, noP)
        result.append("yes" if yesP >= noP else "no")
    return result
# print(table.yesCount, table.noCount)
# trainingTable = getStatistics("../pima.csv")
# matrixTable = sortTable(trainingTable)
# matrixStat = detailData(matrixTable)
# for attr in matrixStat:
#     print(attr[0].mean, attr[0].sd)
#     print(attr[1].mean, attr[1].sd)
#     print()
#     print()
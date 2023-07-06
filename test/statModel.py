class DataModel:
    def __init__(self):
        self.dataLines = []
        self.attrCount = 0
        self.yesCount = 0
        self.noCount = 0

def getStatistics(filename):
    try:
        f = open(filename)
    except FileNotFoundError:
        print("FILE NOT FOUND!")
        return
    
    line = "start reading..."
    table = DataModel()
    while(line != ""):
        line = f.readline().strip()
        if(len(line) == 0):
            break
        data = line.split(",")

        #If we don't know how many attributes we have, initialise the table
        ls = []
        if(len(table.dataLines) == 0):
            for attribute in data:
                if(attribute == "yes" or attribute == "no"):
                    ls.append(attribute)
                    table.dataLines.append(ls)
                    break
                ls.append(float(attribute))
                table.attrCount += 1
            continue
        
        ls = []
        for i in range(0, table.attrCount):
            ls.append(float(data[i]))
        ls.append(data[table.attrCount])
        table.dataLines.append(ls)
    f.close()
    return table

def convertTestTable(filename):
    try:
        f = open(filename)
    except FileNotFoundError:
        print("FILE NOT FOUND!")
        return
    
    line = "start reading..."
    table = DataModel()
    while(line != ""):
        line = f.readline().strip()
        if(len(line) == 0):
            break
        data = line.split(",")
        
        ls = []
        for i in range(len(data)):
            ls.append(float(data[i]))
        table.dataLines.append(ls)
    f.close()
    return table
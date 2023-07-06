import math


class DataModel:
    def __init__(self):
        self.data = []
        self.attrCount = 0

    def get_table(self):
        return self.data

    def get_attr_count(self):
        return self.attrCount

    def get_data_count(self):
        return len(self.data)


class KNNModel:
    def __init__(self, dst, class_type):
        self.dst = dst
        self.class_type = class_type

    def get_dst(self):
        return self.dst

    def set_dst(self, dst):
        self.dst = dst

    def get_class_type(self):
        return self.class_type

    def set_class_type(self, class_type):
        self.class_type = class_type


def read_data(filename):
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

        # If we don't know how many attributes we have, initialise the table
        ls = []
        if(len(table.data) == 0):
            for attribute in data:
                if(attribute == "yes" or attribute == "no"):
                    ls.append(attribute)
                    table.data.append(ls)
                    break
                ls.append(float(attribute))
                table.attrCount += 1
            continue

        ls = []
        for i in range(0, table.attrCount):
            ls.append(float(data[i]))
        ls.append(data[table.attrCount])
        table.data.append(ls)
    f.close()
    return table


def e_dst(testing, training):
    """
    Calculates the euclidian distances between two training types
    """
    #if len(testing) != len(training):
    #    raise TypeError("testing not same type as training")
    
    dst = 0
    for i in range(len(training) - 1):
        # note: we are ignoring the class type by skipping the last obj
        dst += math.pow(training[i] - testing[i], 2)
    return dst


def get_test_data(table):
    """
    Return the first 5 as testing data
    """
    return table[:5]


def get_training_data(table):
    """
    Returns everything after the first 5
    """
    return table[5:]

def get_key_dst(model):
    return model.get_dst()

def knn(testing, training, k):

    results = [] # final output stored here

    
    # calculate distance for our testing data to all our training set
    for i in testing:
        
        # list for our trained data per input
        ls = []

        for j in training:
            # we store the training class type not the testing
            ls.append(KNNModel(e_dst(i, j), j[-1]))

        # we now want to find the k nearest neighbours#
        # we sort the list then pick k
        sorted_ls = sorted(ls, key=get_key_dst)
        nearest = []

        for dt in sorted_ls:
            if len(nearest) >= k:
                break
            nearest.append(dt)
        
        # after we find the k nearest neighbours, we want to classify our input
        # then add it to our list of results to return

        f = 0

        for dt in nearest:
            if dt.get_class_type() == "yes":
                f += 1
            else:
                f -= 1

        if f >= 0:
            results.append("yes")
        else:
            results.append("no")

    if len(results) == 0:
        return None

    return results


def parse_data(file_name):
    with open(file_name, 'r') as fh:
        lines = fh.readlines()


def test():
    data_model = read_data("../pima.csv")
    data_table = data_model.get_table()
    test_data = get_test_data(data_table)
    #print(test_data)
    training_data = get_training_data(data_table)
    #print("---")
    #print(training_data)
    trained = knn(test_data, training_data, 4)



if __name__ == "__main__":
    test()

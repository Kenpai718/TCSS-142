#Kenneth Ahrens
#project2.py

def main():
    #train.csv testing
    in1 = open("train.csv", "r")
    healthTots = [0] * 13 #keep track of all atributes by adding them to a running list
    illTots = [0] * 13
    totCount = [0] * 2 #index 0 = healthy, 1 = ill
    getCount(in1, healthTots, illTots, totCount) #updates above lists with information from file
    totalPatients = totCount[0] + totCount[1] #also counts as number of lines
    hAverages = getAverages(healthTots, totCount[0])
    illAverages = getAverages(illTots, totCount[1])
    sepValues = getSepValues(hAverages, illAverages)

    #calls functions to print information on train.csv
    displayCounts(totalPatients, totCount[0], totCount[1])
    displayLists(hAverages, "Averages of Healthy Patients: ")
    displayLists(illAverages, "Averages of Ill Patients: ")
    displayLists(sepValues, "Seperation Values are: ")
    in1.close()

    in1 = open("train.csv", "r")
    diagCnt = checkAccuracy(in1, sepValues)
    accuracy = round((diagCnt/totalPatients),2) 
    print("Accuracy of Model: {:.2f}({}%)".format(accuracy,accuracy*100))
    in1.close()

    #cleveland testing, writes diagnosis to a file
    in2 = open("cleveland.csv", "r")
    out2 = open("clevelanddiag.csv", "w")
    writeDiagnosis(in2, out2, sepValues)
    in2.close()
    out2.close()


#takes an input file to read from, an output file to write to,
#and seperation values to compare to the input to see if the patient
#is healthy (0) or ill (1), then writes to a csv file the patient's id
#in column 1, and their diagnosis in collumn 2
def writeDiagnosis(i2, o2, sepValues):
    ids = [] #keeps track of patient id
    diagnosis = [] #keeps track of patients diagnosis
    for line in i2: #iterate through input
        data = line.strip().split(",")
        patientID = data[0] #gets their ID from first index
        ids.append(patientID) #adds to end of id list
        attribs = data[1:] #makes new list without patient id
        result = checkDiagnosis(attribs, sepValues) #uses prev function for diagnosis
        diagnosis.append(result) #adds to end of diagnosis list
    #since id/diagnosis list are the same length and correspond with each other
    #a parallel list index can be used to add them to the output file at the same time
    idx = 0
    while idx < len(ids):
        o2.write("{},{}\n".format(ids[idx],diagnosis[idx]))
        idx+=1

#takes an input file and a list containing seperation values
#compares attributes from each patients list to the list of seperation values
#returns how many times the diagnosis was correct
def checkAccuracy(in1, sepValues):
    diagCnt = 0
    for line in in1:
        data = line.strip().split(",")
        attribs = data[:13]
        myDiag = checkDiagnosis(attribs, sepValues)
        realDiag = 0
        if int(data[13]) > 0:
            realDiag = 1
        if myDiag == realDiag:
            diagCnt+=1
    return diagCnt

#takes a list that is assumed to have no diagnosis value and a list of seperation values
#checks to see if patient in the list is healthy (0) or ill (1), returns result as 0 or 1
def checkDiagnosis(attribs, sepValues):
    result = 0
    illAttribCnt = 0
    idx = 0
    while idx < len(attribs):
        el = attribs[idx]
        #if el = ? it will automatically be false
        if el != "?" and float(el) > sepValues[idx]:
            illAttribCnt+=1
        idx+=1
    #they are ill if 6 or more of their attributes were greater then the sepValue attributes
    if illAttribCnt > 6:
        result = 1
    return result
    

#takes a file, a running list of healthy/ill attributes, and a list to keep track of healthy/sick patients
def getCount(i1, hTot, illTot, totCount):
    for line in i1: #iterate through every line in the file
        data = line.strip().split(",") #gets rid of new lines and seperates the line into a list
        attribs = data[:13] #ignores diagnosis attribute
        isIll = 1 #1 for sick, 0 for healthy
        if int(data[13]) == 0:
            isIll = 0
        index = 0
        while index < len(attribs): #iterate through each attribute in the list
            el = attribs[index]
            if el != "?": #if el is "?" nothing will happen because it has a value of 0
                if isIll == 1: #add to running list of healthy attributes
                    illTot[index]+= float(el) 
                else: #add to list of ill attributes
                    hTot[index]+= float(el)
            index+=1
        totCount[isIll]+=1 #isIll counts as the indexing for increasing the count of healthy/sick

#takes two lists and finds the average between each attribute
#then returns the averages of each attribute in a new list
def getSepValues(hAVG,illAVG):
    sepValues = []
    idx = 0
    while idx < len(hAVG):
        average = (hAVG[idx] + illAVG[idx]) / 2.0
        sepValues.append(average)
        idx+=1
    return sepValues

#takes a list of total attributes, the number of patients of that type,
#calculates the averages and then returns them as a list
def getAverages(aList, total):
    newList = []
    idx = 0
    #goes through every element in the list, computes avg, and adds it to a new list
    for el in aList:
        average = float(el) / (total)
        newList.append(average)
    return newList

#takes a list and a string telling what type the list is
#prints the label, then prints the list without [] and seperates with a ","
def displayLists(aList, listType):
    #fence post problem: print the first index to avoid a "," at the end
    print(listType)
    print("{:.2f}".format(aList[0]), end = "") #only prints 2 decimal places
    index = 1
    while index < len(aList):
          print(", {:.2f}".format(aList[index]), end = "")
          index+=1
    print()

#takes 3 parameters that contain a count, and prints it to the corresponding label
def displayCounts(lines, health, ill):
    print("Total Lines Processed:",lines)
    print("Total Healthy Count:", health)
    print("Total Ill Count:", ill)

main()

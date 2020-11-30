#Kenneth Ahrens
#TCSS 142
#5/19/2019
#project1.py
#Takes two napier numbers from user, converts it to an integer, does a calculation, and returns the result as a number and a napier
#Note: I did the extra credit portion which handles the excess "z" problem


z = 2**25 #global variable used for when the result is a huge number and the calculation for int to napier

def main(): #calls functions to execute program
    cont = "y"
    while cont == "y": #loop for program redos
        nap1 = getNapier() #gets napier input from user
        num1 = convertNapToInt(nap1) #converts napier to a number in base 10
        print("The first number is {}".format(num1))
        nap2 = getNapier()
        num2 = convertNapToInt(nap2)
        print("The second number is {}".format(num2))
        oper = getOperator() #get the desired operator from user
        res = doMath(num1,num2,oper) #computes
        napResult = convertIntToNap(res) #gives the final result in napier notation
        print("The result is {} or {}".format(res,napResult))
        cont = input("Do you want to repeat the program? Enter y for yes, n for no: ")

def getNapier(): #get the napier notation from the user
    napier = input("Enter Napier's number: ")
    isNapier = napier.isalpha() and napier.islower()
    while(isNapier == False): #error check, makes sure it is only alphabetical and lowercase
        print("Something is wrong. Try again")
        napier = input("Enter a Napier's number: ")
        isNapier = napier.isalpha() and napier.islower() #exits loop if true
    return napier

def convertNapToInt(napier): #takes a napier number as parameter, converts it to int
    res = 0
    for chr in napier: #checks each letter from the napier number, converts that letter to a number, and adds it to a running sum total
        #gives the power based on ASCII values. Ex: b - a = 98-97 = power 1
        res+= 2**(ord(chr) - ord("a"))
    return res

def convertIntToNap(num): #takes a base 10 number as a parameter, then converts it to napier
    isNeg = False
    if(num < 0): #fixes problem where the function won't run if its negative, converts num to pos
        num += (num * -2)
        isNeg = True
    napierStr = ""
    position = 0 #0 = "a", 25 = "z", represents power of 2
    if num >= z: #handles case where the number is huge and requires a lot of napier z
        napierStr = calcNumZ(num, napierStr)
        num = 0 #ignores the while loop since all the calculations have been finished in the called function
    while num!=0:
        binaryBit = num % 2 #see if bit is 0 or 1
        newNum = num // 2 #convert to base 2
        if binaryBit == 1: #if binary bit is 1, and if it is then add the letter to the string
            letter = chr(position + ord("a")) #pos moves the letter by one each time. Each iteration of pos represents a new base 2 power starting at 2^0
            napierStr+=letter
        num = newNum #moves onto next power in binary
        position+=1 #next letter in alphabet
    if(isNeg == True): #adds a negative sign if it was removed at the start of the function
        napierStr = "-" + napierStr
    return napierStr
    
def calcNumZ(bigNum, napStr): #takes a big number as a parameter and sees how many "z" can fit in it, returns a napier string with the total num of z in napier notation
    numZ = bigNum // z #see how many times 2^25 can fit into the number
    remainder = bigNum % z
    if(numZ > 10): #if the ammount of "z" is greater than 10 then shorten it to a special notation
        napStr = "(z*" + str(numZ) + ")"
    else: #just print the z multiple times
        napStr = "z" * numZ
    if remainder !=0: #calculates the napier notation of the remainder and adds it to the start of the napier string and ends with the ammount of "z"
        remainderNap = convertIntToNap(remainder) #makes use of a previous function to convert it to napier
        napStr = remainderNap + napStr
    return napStr #sends the string back to convertIntToNap
        
    
def getOperator(): #asks user for operator
    operators = "+-*/" #usable operators
    operInput = input("Enter the desired arithmetic operator: ")
    while operInput not in operators: #error check: if something is imputed other then a single valid operator then redo
        print("Something went wrong. Please try again.")
        operInput = input("Enter the desired arithmetic operator: ")
    return operInput
        
def doMath(num1, num2, oper): #checks the operator with if statements and then computes with the two numbers
    if(oper == "/"): #only does interger division because napier can't represent floats
        res = num1 // num2
    elif(oper == "+"):
        res = num1 + num2
    elif(oper == "-"):
        res = num1 - num2
    elif(oper == "*"):
        res = num1 * num2
    return res
        

main() #calls main function

# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 07:09:40 2021

@author: Martin Kovar
"""

def loadTextfile(path):
    with open(path, "r") as file:
        inputList = [line.rstrip() for line in file]
        digitsInOut = []
        for line in inputList:
            left,right = line.split("|")
            digitsInOut.append( (left.split(), right.split()) )
    return digitsInOut

def getSumFromOutputDigits(digitsInOut, searchedDigitLengths):
    total = 0
    for inputDigits,outputDigits in digitsInOut:
        for digit in outputDigits:
            if len(digit) in searchedDigitLengths:
                total += 1
    return total

def decodeOutput(digitsInOut):
    outputValues = []
    # Decode digits
    for inputDigits,outputDigits in digitsInOut:
        numSegments = dict()
        # Get 1,4,7,8: by length
        for idx,digit in enumerate(inputDigits):
            lenDigit = len(digit)
            if lenDigit==2:
                numSegments[1] = digit
            if lenDigit==3:
                numSegments[7] = digit
            if lenDigit==4:
                numSegments[4] = digit
            if lenDigit==7:
                numSegments[8] = digit
        inputDigits.remove(numSegments[1])
        inputDigits.remove(numSegments[7])
        inputDigits.remove(numSegments[4])
        inputDigits.remove(numSegments[8])
        # Get 3: the only digit of length 5 and containing all segments of 1
        for digit in inputDigits:
            if len(digit)==5 and all([char in digit for char in numSegments[1]]):
                numSegments[3] = digit
                inputDigits.remove(digit)
        # Get 9: the only digit of length 6 and containing all segments of 3
        for digit in inputDigits:
            if len(digit)==6 and all([char in digit for char in numSegments[3]]):
                numSegments[9] = digit
                inputDigits.remove(digit)
        # Get 0: the only digit of length 6 and containing all segments of 7
        for digit in inputDigits:
            if len(digit)==6 and all([char in digit for char in numSegments[7]]):
                numSegments[0] = digit
                inputDigits.remove(digit)
        # Get 6: the only remaining digit of length 6
        for digit in inputDigits:
            if len(digit)==6:
                numSegments[6] = digit
                inputDigits.remove(digit)
        # Get 5: the remaining digit whose all segments are contained in 9
        for digit in inputDigits:
            if all([char in numSegments[9] for char in digit]):
                numSegments[5] = digit
                inputDigits.remove(digit)
        # Get 2: the only remaining digit
        numSegments[2] = inputDigits.pop()
        
        # Convert output to numbers
        # Swap dictionary keys and values (I know, it's a terrible way to do it like this)
        numSegmentsRev = dict((v,k) for k,v in numSegments.items())
        valueStr = str()
        for digit in outputDigits:
            for idx,key in enumerate(numSegmentsRev.keys()):
                if sorted(digit)==sorted(key):
                    valueStr += str(numSegmentsRev[key])
        outputValues.append(int(valueStr))
    return outputValues


if __name__ == "__main__":
    inputPath = "input.txt"
    digitsInOut = loadTextfile(inputPath)
    
    searchedDigitLengths = [2,3,4,7]
    sum1478 = getSumFromOutputDigits(digitsInOut, searchedDigitLengths)
    print("Digits 1,4,7,8 appear in total {} times.".format(sum1478))
    
    outputDecoded = decodeOutput(digitsInOut)
    print("Sum of all decoded output values is {}.".format(sum(outputDecoded)))
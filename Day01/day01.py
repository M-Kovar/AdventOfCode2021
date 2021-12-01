# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 12:02:14 2021

@author: mapup
"""


def loadTextfileToList(path):
    with open(path, "r") as file:
        inputList = [int(line.rstrip()) for line in file]
    return inputList

def getNumOfDepthIncreaseSimple(inputList):
    numOfDepthIncrease = 0;
    for (item1, item2) in zip(inputList[:-1], inputList[1:]):
        if item2>item1:
            numOfDepthIncrease += 1  
    return numOfDepthIncrease

def getNumOfDepthIncreaseSlidingWindow(inputList):
    numOfDepthIncrease = 0;
    windowLength = 3
    for i in range(0,len(inputList)-windowLength+1):
        windowA = inputList[i:i+windowLength]
        windowB = inputList[i+1:i+windowLength+1]
        if sum(windowB)>sum(windowA):
            numOfDepthIncrease += 1  
    return numOfDepthIncrease


if __name__ == "__main__":
    inputPath = "input.txt"
    inputList = loadTextfileToList(inputPath)
    
    answerSimple = getNumOfDepthIncreaseSimple(inputList)
    print("getNumOfDepthIncreaseSimple: " + str(answerSimple))
    
    answerSlidingWindow = getNumOfDepthIncreaseSlidingWindow(inputList)
    print("getNumOfDepthIncreaseSlidingWindow: " + str(answerSlidingWindow))
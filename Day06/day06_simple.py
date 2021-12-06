# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 08:20:34 2021

@author: mapup
"""

def loadTextfile(path):
    with open(path, "r") as file:
        inputListStr = file.read()
        inputList = [int(item) for item in inputListStr.split(",")]
    return inputList

def addDay(fishList):
    newFishList = []
    for i in range(0,len(fishList)):
        if fishList[i] > 0:
            fishList[i] -= 1
        else:
            fishList[i] = 6
            newFishList.append(8)
    return fishList + newFishList


if __name__ == "__main__":
    inputPath = "inputExample.txt"
    ageList = loadTextfile(inputPath)
    print("Initial state: {} fish".format(len(ageList)))
    
    numDays = 80
    for i in range(0,numDays):
        ageList = addDay(ageList)
        print("After {} days: {} fish".format(i+1,len(ageList)))
        # Use exponential growth: each fish of the first ones grows exponentially
        # --> calculate with just those (offsprings as individuals are not important)
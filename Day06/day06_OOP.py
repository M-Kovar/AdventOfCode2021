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


class FishSimulator:
    def __init__(self, ageUntilBabiesList):
        self.ageUntilBabiesList = ageUntilBabiesList
        self.fishList = self.createFishList(ageUntilBabiesList)
        self.dayCounter = 0
        self.fishCounter = 0
        print("Initial state: {}".format(self.fishList))
        
    def createFishList(self, ageUntilBabiesList):
        fishList = []
        for a in ageUntilBabiesList:
            fishList.append(Fish(a))
        return fishList
        
    def addDay(self):
        newFishList = []
        for fish in self.fishList:
            newFish = fish.addDay()
            if newFish:
                newFishList.append(newFish)
        self.fishList += newFishList
        self.dayCounter += 1
        print("After {} days: {} fish".format(self.dayCounter,self.getNumberOfFish()))
    
    def getNumberOfFish(self):
        return len(self.fishList)

class Fish:
    def __init__(self, ageUntilBabies):
        self.ageUntilBabies = ageUntilBabies
        
    def addDay(self):
        if self.ageUntilBabies>0:
            self.ageUntilBabies -= 1
            newFish = None
        else:
            self.ageUntilBabies = 6
            newFish = Fish(8)
        return newFish

if __name__ == "__main__":
    inputPath = "inputExample.txt"
    ageUntilBabiesList = loadTextfile(inputPath)
    
    numDays = 80
    fishSim = FishSimulator(ageUntilBabiesList)
    for i in range(0,numDays):
        fishSim.addDay()
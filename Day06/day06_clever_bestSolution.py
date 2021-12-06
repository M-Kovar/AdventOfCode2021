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

class FishRegister:
    
    def __init__(self, ageList, fishAges=range(0,9)):
        # Initialize empty dict
        fishDict = self.initializeEmptyDict(fishAges)
        # populate with fish numbers
        for age in ageList:
            fishDict[age] += 1
        self.fishDict = fishDict
        self.dayCounter = 0
        self.ageList = ageList
        self.fishAges = fishAges
        
    def addDay(self):
        updatedFishDict = self.initializeEmptyDict(self.fishAges)
        # Sort out 0-day birth-giving fish and the new generation
        updatedFishDict[6] = self.fishDict[0] # Restart 0-day fish to day 6
        updatedFishDict[max(self.fishAges)] = self.fishDict[0] # Add babies to "day 8" category
        # Move all other fish 1 day closer to birth-giving day
        for i in self.fishAges[1:]:    # Starts with index 1 to skip 0-day fish
            updatedFishDict[i-1] += self.fishDict[i]
        self.fishDict = updatedFishDict
        self.dayCounter += 1
    
    def initializeEmptyDict(self, fishAges):
        fishDict = dict()
        for ageKey in fishAges:
            fishDict[ageKey] = 0
        return fishDict
    
    def getTotal(self):
        total = 0
        for fish in self.fishDict:
            total += self.fishDict[fish]
        return total
    
    def getDict(self):
        return self.fishDict
    
    def printStatus(self):
        print("Day {} status (age: amount):".format(self.dayCounter))
        print(self.fishDict)
        return



if __name__ == "__main__":
    inputPath = "input.txt"
    ageList = loadTextfile(inputPath)
    print("Initial state: {} fish".format(len(ageList)))
    
    numDays = 256
    fishRegister = FishRegister(ageList)
    fishRegister.printStatus()
    fishDict = fishRegister.getDict()
    
    for day in range(0,numDays):
        fishRegister.addDay()
        fishRegister.printStatus()
        print("\n")
       
    totalFish = fishRegister.getTotal()
    print("Total number after {} days: {} fish".format(numDays,totalFish))
    
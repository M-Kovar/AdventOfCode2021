# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 07:09:40 2021

@author: Martin Kovar
"""

def loadTextfile(path):
    inputListInt = []
    with open(path, "r") as file:
        # In each stripped read line, read characters and convert to list of integers
        inputListInt = [[int(char) for char in line.rstrip()] for line in file]
    return inputListInt

class FlashingOctopusMatrix:
    
    def __init__(self, octopusList):
        self.octopusList = octopusList
        self.stepCounter = 0
        self.flashCounter = 0
        self.numRows,self.numCols = self.getNumRowsCols(octopusList)

    def addStep(self):
        # First, the energy level of each octopus increases by 1
        self.octopusList = [[num+1 for num in line] for line in self.octopusList]
        # Then, any octopus with an energy level greater than 9 flashes
        continueFlashing = True
        alreadyFlashed = set()
        while continueFlashing:
            flashCoords = self.findFlashing()
            for xyCoords in flashCoords:
                if xyCoords not in alreadyFlashed:
                    self.flash(xyCoords)
                    alreadyFlashed.add(xyCoords)
            continueFlashing = bool(flashCoords)
        # Set fish that flashed to 0:
        for x,y in alreadyFlashed:
            self.octopusList[y][x] = 0
        self.stepCounter += 1
        
    def findFlashing(self):
        flashCoords = []
        for y in range(0,self.numRows):
            for x in range(0,self.numCols):
                if self.octopusList[y][x] > 9:
                    flashCoords.append((x,y))
        return flashCoords

    def flash(self, xyCoords):
        x,y = xyCoords
        # Update the flashing octopus
        self.flashCounter += 1
        self.octopusList[y][x] = 0
        # Update the neighboring octopuses
        for yOffset in range(-1,2):
            for xOffset in range(-1,2):
                if not (xOffset==0 and yOffset==0): # Skip the flashing point at [0][0]
                    xRel,yRel = x+xOffset, y+yOffset
                    if (xRel>=0 and xRel<self.numCols) and (yRel>=0 and yRel<self.numRows):
                        self.octopusList[yRel][xRel] += 1
        return
    
    def isSynced(self):
        sumAll = sum([sum(line) for line in self.octopusList])
        return sumAll==0
                
    def getNumRowsCols(self, lst):
        return ( len(lst), len(lst[0]) )
        
    def printStatus(self):
        print("After step {}:".format(self.stepCounter))
        [print(line) for line in self.octopusList]
        print("\n")
    
    def getNumFlashes(self):
        return self.flashCounter
    

if __name__ == "__main__":
    inputPath = "input.txt"
    inputList = loadTextfile(inputPath)

    numSteps = 500
    octMat = FlashingOctopusMatrix(inputList)
    print("Initial status (step 0):")
    octMat.printStatus()
    for step in range(1,numSteps+1):
        octMat.addStep()
        octMat.printStatus()
        if octMat.isSynced():
            print("Dumbos got successfully synchronized after {} steps!".format(step))
            break
    
    print("Number of flashes after {} steps: {}".format(step,octMat.getNumFlashes()))
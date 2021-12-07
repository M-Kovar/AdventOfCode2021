# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 06:56:47 2021

@author: Martin Kovar
"""

def loadTextfile(path):
    with open(path, "r") as file:
        inputListStr = file.read()
        inputList = [int(item) for item in inputListStr.split(",")]
    return inputList

def getBestPosition(positions,method=2):
    possiblePositions = range(0,max(positions)+1)
    fuelNeeded = [0] *len(possiblePositions)
    for possiblePos in possiblePositions:
        for pos in positions:
            distance = abs(pos - possiblePos)
            if method==1:
                fuelNeeded[possiblePos] += distance
            else:
                fuelNeeded[possiblePos] += int( (distance*(distance+1))/2 ) # Using arithmetic series formula
                #fuelNeeded[possiblePos] += sum(list(range(0,distance+1))) # Using simple list sum
    bestPosition = fuelNeeded.index(min(fuelNeeded))
    return bestPosition,fuelNeeded
        

if __name__ == "__main__":
    inputPath = "input.txt"
    positions = loadTextfile(inputPath)
    
    bestPositionSimple,fuelNeededSimple = getBestPosition(positions,method=1)
    print("Best position to align friendly crabs [method 1]: {}".format(bestPositionSimple))
    print("Fuel needed [method 1]: {}".format(fuelNeededSimple[bestPositionSimple]))
    
    bestPosition,fuelNeeded = getBestPosition(positions,method=2)
    print("Best position to align friendly crabs [method 2]: {}".format(bestPosition))
    print("Fuel needed [method 2]: {}".format(fuelNeeded[bestPosition]))
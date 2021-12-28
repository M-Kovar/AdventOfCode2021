# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 07:09:40 2021

@author: Martin Kovar
"""

import math

def loadTextfile(path):
    with open(path, "r") as file:
        inputList = [line.rstrip() for line in file]
    return inputList

def getLowestPoints(basinMap):
    numRows = len(basinMap)
    numCols = len(basinMap[0])
    lowestPoints = dict()
    for x in range(0,numCols):
        for y in range(0,numRows):
            centerPointValue = int(basinMap[y][x])
            neighborCoords = getNeighborPointsCoordinates((x,y))
            neighborValues = []
            for (xN,yN) in neighborCoords:
                if areValidCoordinates(xN,yN,basinMap):
                    neighborValues.append(int(basinMap[yN][xN]))
            if centerPointValue < min(neighborValues):
                lowestPoints[(x,y)] = centerPointValue
    return lowestPoints
            
def getBasinSizes(basinMap):
    lowestPoints = getLowestPoints(basinMap)
    basinSizes = []
    for (x,y),value in lowestPoints.items():
        lowestPointCoords = (x,y)
        basinPoints = getBasinPoints(lowestPointCoords,basinMap,searchedBasinPoints=[])
        # print(basinPoints)
        basinSizes.append(len(basinPoints))
    return basinSizes
        
def getBasinPoints(centerPointXy,basinMap,searchedBasinPoints):
    neighborCoords = getNeighborPointsCoordinates(centerPointXy)
    for (x,y) in neighborCoords:
        if areValidCoordinates(x,y,basinMap): # Move this check into a separate function  
            neighborValue = int(basinMap[y][x])
            if neighborValue == 9 or (x,y) in searchedBasinPoints:
                # Skip basin edges or already-searched points
                continue
            else:
                # Recursively search in the neighborhood of the current point
                searchedBasinPoints.append((x,y))
                getBasinPoints((x,y),basinMap,searchedBasinPoints)
    return searchedBasinPoints

def getNeighborPointsCoordinates(centerPointXy):
    x,y = centerPointXy
    up = (x,y-1)
    down = (x,y+1)
    left = (x-1,y)
    right = (x+1,y)
    return [up,down,left,right]
    

def areValidCoordinates(x,y,basinMap):
    numRows = len(basinMap)
    numCols = len(basinMap[0])
    return (x>=0 and x<=numCols-1) and (y>=0 and y<=numRows-1)

def getRiskLevels(lowestPoints):
    # Risk level = lowest points height increased by 1
    return [num+1 for num in lowestPoints.values()]

def getBasinSizesScore(basinSizes):
    threeLargest = sorted(basinSizes)[-3:]
    return math.prod(threeLargest)



if __name__ == "__main__":
    inputPath = "input.txt"
    basinMap = loadTextfile(inputPath)
    
    lowestPoints = getLowestPoints(basinMap)
    riskLevels = getRiskLevels(lowestPoints)
    print("Sum of risk levels: {}".format(sum(riskLevels)))
    
    basinSizes = getBasinSizes(basinMap)
    basinSizesScore = getBasinSizesScore(basinSizes)
    print("Basin sizes multiplied by each other: {}".format(basinSizesScore))
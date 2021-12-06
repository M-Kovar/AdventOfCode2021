# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 09:14:34 2021

@author: mapup
"""

def loadTextfile(path):
    with open(path, "r") as file:
        inputList = [line.rstrip() for line in file]
    return inputList

def processInput(inputTxt):
    linePoints = []
    for line in inputTxt:
        startEnd = line.split(" -> ")
        xyStart = startEnd[0].split(",")
        xyEnd = startEnd[1].split(",")
        startNums = ( int(xyStart[0]), int(xyStart[1]) )
        endNums = ( int(xyEnd[0]), int(xyEnd[1]) )
        linePoints.append((startNums,endNums))
    return linePoints

def getDiagram(linePoints):
    diagram = initializeEmptyDiagram(linePoints)
    for line in linePoints:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[1][0]
        y2 = line[1][1]
        xStep = 1 if x1<=x2 else -1
        yStep = 1 if y1<=y2 else -1
        xCoords = list(range(x1,x2+xStep,xStep))
        yCoords = list(range(y1,y2+yStep,yStep))
        # Horizontal/vertical:
        if x1==x2 or y1==y2:
            for x in xCoords:
                for y in yCoords:
                    diagram[y][x] += 1
        # Diagonal:
        else:
            for x,y in zip(xCoords,yCoords):
                diagram[y][x] += 1
                pass
    return diagram

def initializeEmptyDiagram(linePoints):
    #numRows = len(linePoints)
    numCols = getMaxNumber(linePoints)+1
    numRows = numCols
    diagram = [ [0]*numCols for i in range(numRows)]
    #diagram = [[0]*numCols]*numRows # Don't use this, it's a trap! This copies just a reference of the list being multiplied
    return diagram

def countOverlapPoints(diagram, minOverlap):
    overlapCounter = 0
    for row in diagram:
        #print(row)
        for num in row:
            if num >= minOverlap:
                overlapCounter += 1
            #print((num,overlapCounter))
    return overlapCounter

def getMaxNumber(linePoints):
    return max(max(max(linePoints)))


if __name__ == "__main__":
    inputPath = "input.txt"
    inputTxt = loadTextfile(inputPath)
    linePoints = processInput(inputTxt)
    
    diagram = getDiagram(linePoints)
    minOverlap = 2
    overlapSum = countOverlapPoints(diagram,minOverlap)
    print("Number of points where at least {} lines overlap: {}".format(minOverlap,overlapSum))
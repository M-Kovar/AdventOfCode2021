# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 07:09:40 2021

@author: Martin Kovar
"""

def loadTextfile(path):
    points = []
    folds = []
    with open(path, "r") as file:
        lines = [line.rstrip() for line in file]
        for line in lines:
            if "," in line:
                x,y = line.split(",")
                points.append( (int(x),int(y)) )
            elif "fold" in line:
                axis,num = line.split()[2].split("=")
                folds.append( (axis,int(num)) )
    return points,folds

def foldOrigami(points,folds,maxSteps=float("inf")):
    pointsFolded = points
    for stepNum,(axis,numFold) in enumerate(folds):
        # Stop if number of steps was reached
        if stepNum > maxSteps-1:
            break
        pointsTemp = []
        for x,y in pointsFolded:
            xNew,yNew = x,y
            # Omit points that are on the folding line:
            if (axis=="x" and x==numFold) or (axis=="y" and y==numFold):
                continue
            if axis=="x" and x > numFold:
                xNew = x - (x-numFold)*2
            elif axis=="y" and y > numFold:
                yNew = y - (y-numFold)*2
            pointsTemp.append((xNew,yNew))
        # Convert to set and back to remove overlapping points
        pointsFolded = list(set(pointsTemp.copy()))
    return pointsFolded
                
def printOrigamiPoints(origamiPoints,emptyChar=" ",filledChar="▓"):
    # Interesting characters to try out: ░,▓,█,▐,■
    maxX,maxY = getGridBoundaries(origamiPoints)
    # Prepare the grid for printing - filled with empty characters
    printList = [[emptyChar for pos in range(0,maxX+1)] for line in range(0,maxY+1)]
    for x,y in origamiPoints:
        printList[y][x] = filledChar
    for line in printList:
        print("".join(line))
    return printList
    
def getGridBoundaries(points):
    allX = [x for x,y in points]
    allY = [y for x,y in points]
    return max(allX),max(allY)



if __name__ == "__main__":
    inputPath = "input.txt"
    points,folds = loadTextfile(inputPath)
    
    origamiPoints1Step = foldOrigami(points,folds,maxSteps=1)
    print("Number of points after first fold: {}".format(len(origamiPoints1Step)))
    
    origamiPoints = foldOrigami(points,folds)
    # maxX,maxY = getGridBoundaries(origamiPoints)
    printList = printOrigamiPoints(origamiPoints)
    
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 07:11:50 2021

@author: mapup
"""

def loadTextfileToDirections(path):
    with open(path, "r") as file:
        directions = [line.rstrip().split() for line in file]
    return directions

def getPosition(directions):
    position = [0,0]    # [0]: forward position, [1]: depth
    for line in directions:
        direction = line[0]
        numSteps = int(line[1])
        if direction == "forward":
            position[0] += numSteps
        if direction == "down":
            position[1] += numSteps
        elif direction == "up":
            position[1] -= numSteps
    return position

def getPositionWithAim(directions):
    position = [0,0]    # [0]: forward position, [1]: depth
    aim = 0
    for line in directions:
        direction = line[0]
        numSteps = int(line[1])
        if direction == "forward":
            position[0] += numSteps
            position[1] += numSteps*aim
        elif direction == "down":
            aim += numSteps
        elif direction == "up":
            aim -= numSteps
    return position


if __name__ == "__main__":
    inputPath = "input.txt"
    directions = loadTextfileToDirections(inputPath)
    #directions = [["forward",5],["down",5],["forward",8],["up",3],["down",8],["forward",2]]
    position = getPosition(directions)    # [0]: forward position, [1]: depth
    positionWithAim = getPositionWithAim(directions)
    
    answer1 = position[0] * position[1]
    print("Position*depth: " + str(answer1))
    
    answer2 = positionWithAim[0] * positionWithAim[1]
    print("Position*depth: " + str(answer2))
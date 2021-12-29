# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 07:09:40 2021

@author: Martin Kovar
"""

import numpy as np
from queue import PriorityQueue

def loadTextfile(path):
    with open(path, "r") as file:
        caveMap = [[int(char) for char in line.rstrip()] for line in file]   
    return np.asarray(caveMap)

def findLowestRisk_notBest(caveMap):
    # Heavily inspired by https://www.techiedelight.com/find-minimum-cost-reach-last-cell-matrix-first-cell/
    numRows = len(caveMap)
    numCols = len(caveMap[0])
    # Initialize cost matrix
    costs = np.zeros((numRows,numCols),int)
    # Fill the cost matrix
    for y in range(numRows):
        for x in range(numCols):
            costs[y][x] = caveMap[y][x]
            # Filling of the first row (elements can only be reached from left):
            if y == 0 and x > 0:
                costs[0][x] += costs[0][x-1]
            # Filling of the first column (elements can only be reached from up):
            elif x == 0 and y > 0:
                costs[y][0] += costs[y-1][0]
            # Filling of all other elements (can be reached from top or from left):
            elif x > 0 and y > 0:
                costs[y][x] += min(costs[y-1][x], costs[y][x-1])
            # Special case for not counting the start point (being the last elif to avoid unnecessary frequent evaluation):
            elif x==0 and y==0:
                costs[0][0] = 0
    # Lowest risk is stored in the last costs element
    lowestRisk = costs[-1][-1]
    return lowestRisk, costs


def findLowestRisk_Astar(cave_map):
    # Adopted from https://github.com/Farbfetzen/Advent_of_Code/blob/main/python/2021/day15.py
    # Pathfinding using A*
    numRows = len(cave_map)
    numCols = len(cave_map[0])
    start = (0, 0)
    destination = (numCols - 1, numRows - 1)
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    risk_so_far = {start: 0}
    offsets = ((1, 0), (0, 1), (-1, 0), (0, -1))
    pos = None
    while not frontier.empty():
        pos = frontier.get()[1]
        if pos == destination:
            break
        for offset in offsets:
            new_pos = (pos[0] + offset[0], pos[1] + offset[1])
            if 0 <= new_pos[0] < numCols and 0 <= new_pos[1] < numRows:
                new_risk = risk_so_far[pos] + cave_map[new_pos[1]][new_pos[0]]
                if new_pos not in came_from or new_risk < risk_so_far[new_pos]:
                    risk_so_far[new_pos] = new_risk
                    priority = new_risk + manhattan_distance(new_pos, destination)
                    frontier.put((priority, new_pos))
                    came_from[new_pos] = pos
    return risk_so_far[pos]


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def expandMap(caveMap,expandFactor=5):
    # Solved using Numpy
    caveMapTileOrig = caveMap.copy()
    caveMapExpanded = np.asarray([])
    for r in range(expandFactor):
        caveMapTile = caveMapTileOrig.copy() + r-1
        caveMapNewRow = np.asarray([])
        for c in range(expandFactor):
            caveMapTile += 1
            # Wrap all values >=9 back to 1 and higher:
            caveMapTile[caveMapTile>9] = caveMapTile[caveMapTile>9] % 9
            # Append the new tile to the right end of the cave map new row
            if caveMapNewRow.size > 0:
                caveMapNewRow = np.concatenate((caveMapNewRow,caveMapTile.copy()),1)
            else:
                caveMapNewRow = caveMapTile.copy()
        # Append the new row to the bottom of the cave map:
        if caveMapExpanded.size > 0:
            caveMapExpanded = np.concatenate((caveMapExpanded,caveMapNewRow.copy()))
        else:
            caveMapExpanded = caveMapNewRow.copy()
    return caveMapExpanded



if __name__ == "__main__":
    inputPath = "input.txt"
    caveMap = loadTextfile(inputPath)


    # Dynamic programming algorithm (does not find the best possible path) - Part 1
    lowestRisk_notBest,costs_notBest = findLowestRisk_notBest(caveMap)
    print("Lowest risk in basic map (Dynamic programming algo.): {}".format(lowestRisk_notBest))
    # The correct answer was 720...but why? This gives 722
    
    # Dynamic programming algorithm (does not find the best possible path) - Part 2
    caveMapExpanded = expandMap(caveMap)
    lowestRiskExpanded_notBest,costsExpanded_notBest = findLowestRisk_notBest(caveMapExpanded)
    print("Lowest risk in full map (Dynamic programming algo.): {}".format(lowestRiskExpanded_notBest))
    # The correct answer was 3025...but why? This gives 3040

    
    # A-star implementation (solution adopted from another AoC participant :-( ) - Part 1
    lowestRisk = findLowestRisk_Astar(caveMap)
    print("Lowest risk in basic map (A* algo.): {}".format(lowestRisk))
    # Gives correct answer
    
    # A-star implementation (solution adopted from another AoC participant :-( ) - Part 2
    lowestRiskExpanded = findLowestRisk_Astar(caveMapExpanded)
    print("Lowest risk in full map (A* algo.): {}".format(lowestRiskExpanded))
    # Gives correct answer
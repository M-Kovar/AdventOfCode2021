# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 07:09:40 2021

@author: Martin Kovar
"""

import timeit

def loadTextfile(path):
    pathMap = []
    with open(path, "r") as file:
        # Load cave paths as tuples
        pathMap = [tuple(line.rstrip().split("-")) for line in file]
    return pathMap

def findPaths(pathMapIn,maxSingleSmallCaveVisits=1,maxTotalSmallCaveVisits=float('inf')):
    pathsFinal =[]
    # As a starting point, create paths starting at "start"
    paths = [[*startEnd] for startEnd in pathMapIn if startEnd[0]=="start"]
    # Add paths that are in "x-start" format:
    paths.extend( [[*reversed(startEnd)] for startEnd in pathMapIn if startEnd[1]=="start"] )
    # Remove paths with "start" to avoid going back to start
    pathMap = list( filter(lambda startEnd: "start" not in startEnd, pathMapIn) )
    # Loop through created paths
    continueSearching = True
    while continueSearching:
        pathsExtended = []
        for path in paths:
            pathEnd = path[-1]
            for cave1,cave2 in pathMap:
                # Validity check: limit of single or total small cave visits must not be reached
                smallCaveLimitValid = not (singleSmallCaveVisitLimitReached(path,pathEnd,maxSingleSmallCaveVisits) or totalSmallCaveVisitLimitReached(path,pathEnd,maxTotalSmallCaveVisits))
                if pathEnd == cave1 and smallCaveLimitValid:
                    pathsExtended.append( path + [cave2] )
                elif pathEnd == cave2 and smallCaveLimitValid:
                    pathsExtended.append( path + [cave1] )
                # Skip path if path validity conditions are not met
                else:
                    continue
                # Move paths ending with "end" to the list of finalized paths
                if pathsExtended[-1][-1] == "end":
                    pathsFinal.append( pathsExtended.pop() )
        paths = pathsExtended
        print("Paths found so far: {}".format(len(pathsFinal)))
        # Continue searching if there are still non-finalized paths
        continueSearching = bool(paths)
    return pathsFinal
    
def areAllPathsEnded(paths):
    pathsWithEnds = [path for path in paths if path[-1]=="end"]
    return len(pathsWithEnds) == len(paths)

def singleSmallCaveVisitLimitReached(path,caveName,maxVisits=1):
    return getSmallCaves(path).count(caveName) > maxVisits
    
def totalSmallCaveVisitLimitReached(path,caveName,maxVisits=float('inf')):
    smallCaves = getSmallCaves(path)
    # Check based on number of duplicate caves
    # This may not work for maxVisits other than 1 and inf (was too afraid to try)
    return len(smallCaves) - len(set(smallCaves)) > maxVisits

def getSmallCaves(path):
    return [cave for cave in path if cave.islower() and cave not in ["start","end"]]



if __name__ == "__main__":
    inputPath = "input.txt"
    pathMap = loadTextfile(inputPath)

    start1 = timeit.default_timer()
    paths1 = findPaths(pathMap)
    stop1 = timeit.default_timer()
    print("Number of paths found (small caves visited max once): {}".format(len(paths1)))
    print("Crawling through all the caves took {:.5f} seconds".format(stop1-start1))
    print("\n")
    
    start2 = timeit.default_timer()
    paths2 = findPaths(pathMap, maxSingleSmallCaveVisits=2, maxTotalSmallCaveVisits=1)
    stop2 = timeit.default_timer()
    print("Number of paths found (single small cave visited max twice, any other small ones just once): {}".format(len(paths2)))
    print("Crawling through all the caves took {:.5f} seconds".format(stop2-start2))
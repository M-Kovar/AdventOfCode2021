# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 07:09:40 2021

@author: Martin Kovar
"""

# Ast: Abstract Syntax Trees (https://docs.python.org/3/library/ast.html)
# Ast can be used to convert the snailfish number strings into nested lists
import ast
import re
import math


def loadTextfile(path, convertToLists=False):
    with open(path, "r") as file:
        # Return numbers as nested lists
        # Note: snum = snailfish number
        snums = [ast.literal_eval(line.strip()) for line in file]
        # If requested, convert to nested lists representation (not used in day18)
        if convertToLists:
            snums = [ast.literal_eval(line) for line in snums]
    return snums


def getHomeworkDonePart1(snums):
    # Add and reduce all numbers
    snumFinal = snums[0]
    for snum in snums[1:]:
        snumFinal = addSnum(snumFinal, snum)
        snumFinal = reduceSnum(snumFinal)
    return snumFinal

def getHomeworkDonePart2(snums):
    # Find the largest magnitude of any two snums
    maxMag = 0
    for snum1 in snums:
        for snum2 in snums:
            snumPair = [snum1,snum2]
            mag = getMagnitude(getHomeworkDonePart1(snumPair))
            maxMag = max(mag, maxMag)
    return maxMag

def addSnum(snum, snumToAdd):
    return "[{},{}]".format(snum, snumToAdd)


def reduceSnum(snum):
    reduce = True
    snumPrev = snum
    while reduce:
        snum = explodeSnum(snum, explodeAll=True)
        # Do a single split only when all explodes are done or not applicable
        snum = splitSnum(snum)
        reduce = snumPrev != snum
        snumPrev = snum
    return snum


def explodeSnum(snum, nestLevelToExplode=5, explodeAll=False):
    # explodeAll==False: Explodes only the first snum found
    # explodeAll==True: Explodes all explodable snums at once
    nestLevel = 0
    # Find the nest level and position of the deepest nest
    for pos, char in enumerate(snum):
        if char == "[":
            nestLevel += 1
            if nestLevel == nestLevelToExplode:
                pairStart = pos
        elif char == "]":
            if nestLevel == nestLevelToExplode:
                pairEnd = pos
                break
            else:
                nestLevel -= 1
    # Return the original number if explosion is not applicable
    else:
        return snum
    # Explode the deepest nest
    # Get numbers from the nested pair
    pair = tuple([int(i) for i in snum[pairStart+1:pairEnd].split(",")])
    pairNew = "0"
    # Find and replace the closest number to the left (if any) and add
    leftPart = snum[:pairStart]
    rightPart = snum[pairEnd+1:]
    resLeft = re.search(re.compile("[0-9]+(?!.*[0-9]+)"), leftPart) # "pattern(?!.*pattern)" searches for the last match
    resRight = re.search(re.compile("[0-9]+"), rightPart)
    # Find and replace the closest number from the nested pair to the left (if any)
    if resLeft:
        leftNumNew = str(int(resLeft[0]) + pair[0])
        leftNumPos = resLeft.span()
        leftPartNew = leftPart[:leftNumPos[0]] + leftNumNew + leftPart[leftNumPos[1]:]
    else:
        leftPartNew = leftPart
    # Find and replace the closest number from the nested pair to the right (if any)
    if resRight:
        rightNumNew = str(int(resRight[0]) + pair[1])
        rightNumPos = resRight.span()
        rightPartNew = rightPart[:rightNumPos[0]] + rightNumNew + rightPart[rightNumPos[1]:]
    else:
        rightPartNew = rightPart
    snumExploded = leftPartNew + pairNew + rightPartNew
    # If requested, repeat explosions until all are done
    if explodeAll:
        snumExploded = explodeSnum(snumExploded, explodeAll=True)
    return snumExploded


def splitSnum(snum, splitAll=False):
    # splitAll==False: Splits only the first snum found
    # splitAll==True: Splits all splittable snums at once
    numsToSplit = re.search("[0-9][0-9]", snum)
    if numsToSplit:
        num = int(numsToSplit[0])
        numStart,numEnd = numsToSplit.span()
        numNew = "[{},{}]".format(math.floor(num/2), math.ceil(num/2))
        snum = snum[:numStart] + numNew + snum[numEnd:]
        # If requested, repeat splits until all are done
        if splitAll:
            snum = splitSnum(snum, splitAll=True)
    # Return the original number if split is not applicable
    return snum


def getMagnitude(snum):
    continueCalculation = True
    while continueCalculation:
        # Find any first pair, replace it with its magnitude and continue until all are processed
        for pos, char in enumerate(snum):
            if char == "[":
                pairStart = pos
            elif char == "]":
                pairEnd = pos
                break
        pair = tuple([int(i) for i in snum[pairStart+1:pairEnd].split(",")])
        pairMagnitude = pair[0]*3 + pair[1]*2
        snum = snum[:pairStart] + str(pairMagnitude) + snum[pairEnd+1:]
        continueCalculation = "[" in snum
    magnitude = int(snum)
    return magnitude

# -----
# Tests
# Adopted from the dearest and kindest Jana Zahradnickova
def testAll():
    testSplit()
    testExplode()
    testReduce()
    print("All test passed.")

def testExplode():
    assert explodeSnum("[[[[[9,8],1],2],3],4]") == "[[[[0,9],2],3],4]"
    assert explodeSnum("[7,[6,[5,[4,[3,2]]]]]") == "[7,[6,[5,[7,0]]]]"
    assert explodeSnum("[[6,[5,[4,[3,2]]]],1]") == "[[6,[5,[7,0]]],3]"
    assert explodeSnum("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
    assert explodeSnum("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"
    assert explodeSnum("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]") == "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"
    assert explodeSnum("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]") == "[[[[0,7],4],[15,[0,13]]],[1,1]]"
    assert explodeSnum("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"


def testSplit():
    assert splitSnum("[[[[0,7],4],[15,[0,13]]],[1,1]]") == "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"
    assert splitSnum("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]") == "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"


def testReduce():
    assert reduceSnum("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    assert reduceSnum(addSnum("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]", "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]")) == "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"
# -----


if __name__ == "__main__":
    inputPath = "input.txt"
    # snum = snailfish number
    snums = loadTextfile(inputPath)
    
    snumFinal = getHomeworkDonePart1(snums)
    print("Final snum: " + snumFinal)
    snumMagnitude = getMagnitude(snumFinal)
    print("Magnitude of the resulting snailfish number is: {}".format(snumMagnitude))
    
    largestMagnitude = getHomeworkDonePart2(snums)
    print("Largest magnitude of any two snums: {}".format(largestMagnitude))
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 07:09:40 2021

@author: Martin Kovar
"""

def loadTextfile(path):
    with open(path, "r") as file:
        inputList = [line.rstrip() for line in file]
    return inputList

def getIllegalChars(inputList):
    # Inspired by https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-an-expression/
    illegalCharsList = [None]*len(inputList)
    leftBrackets = "([{<"
    rightBrackets = ")]}>"
    # Gather all left and right brackets:
    for lineIdx,line in enumerate(inputList):
        brList = []
        for char in line:
            if char in leftBrackets:
                brList.append(char)
            elif char in rightBrackets:
                lastLeftBr = brList.pop()
                if lastLeftBr != getPairBracket(char):
                    illegalCharsList[lineIdx] = char
                    break
    return illegalCharsList

def autocomplete(inputList):
    leftBrackets = "([{<"
    rightBrackets = ")]}>"
    addedCharsList = []
    for lineIdx,line in enumerate(inputList):
        brList = []
        addedCharsList.append([])
        for char in line:
            if char in leftBrackets:
                brList.append(char)
            elif char in rightBrackets:
                # Find first/any pair bracket and remove from list (reverse done to remove last occurence of char instead of first):
                brList.reverse()
                brList.remove(getPairBracket(char))
                brList.reverse()
        # Complement brackets left in the list (start from the end to maintain the order):
        brList.reverse()
        for char in brList:
            addedCharsList[lineIdx].append(getPairBracket(char))
    return addedCharsList

def getPairBracket(bracket):
    leftBrackets = "([{<"
    rightBrackets = ")]}>"
    if bracket in leftBrackets:
        pairBracket = rightBrackets[leftBrackets.index(bracket)]
    elif bracket in rightBrackets:
        pairBracket = leftBrackets[rightBrackets.index(bracket)]
    return pairBracket

def getScoreIllegal(illegalCharsList):
    charsScore = { ")":3, 
                   "]":57,
                   "}":1197,
                   ">":25137 }
    scoreTotal = sum([charsScore[char] for char in illegalCharsList if char])
    return scoreTotal

def getScoreAutocomplete(addedCharsList):
    scoreList = []
    multiplier = 5
    charsScore = { ")":1, 
                   "]":2,
                   "}":3,
                   ">":4 }
    for lineIdx,line in enumerate(addedCharsList):
        score = 0
        for char in line:
            score *= multiplier
            score += charsScore[char]
        scoreList.append(score)
    middleIdx = int(len(scoreList)/2) # Round down to nearest integer
    return sorted(scoreList)[middleIdx]


if __name__ == "__main__":
    inputPath = "input.txt"
    inputList = loadTextfile(inputPath)
    
    # Count score of illegal characters in corrupted lines
    illegalCharsList = getIllegalChars(inputList)
    scoreIllegal = getScoreIllegal(illegalCharsList)
    print("Score of illegal characters: {}".format(scoreIllegal))
    
    # Count score of autocomplete characters for incomplete lines
    # Get only the non-corrupted lines
    incompleteLines = [line for illChar,line in zip(illegalCharsList,inputList) if not illChar]
    addedCharsList = autocomplete(incompleteLines)
    scoreAutocomplete = getScoreAutocomplete(addedCharsList)
    print("Score of autocompleted characters: {}".format(scoreAutocomplete))
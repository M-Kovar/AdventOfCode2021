# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 06:52:33 2021

@author: mapup
"""


def loadBinaryInput(path):
    with open(path, "r") as file:
        lines = [line.rstrip().split() for line in file]
    return lines

def getGammaEpsilon(binInput):
    wordLength = len(binInput[0][0])
    gammaBin = str()
    epsilonBin = str()
    for pos in range(0,wordLength):
        prevSym = getPrevalentSymbol(binInput, pos)
        gammaBin += prevSym
        epsilonBin += getSymbolNegation(prevSym)
    return gammaBin,epsilonBin

def getOxygenRate(binInput):
    binSel = binInput
    wordLength = len(binInput[0][0])
    for pos in range(0,wordLength):
        mostCommonSym = getPrevalentSymbol(binSel, pos, "1")
        if mostCommonSym=="equal":
            mostCommonSym = "1"
        binSel = selectCompliantWords(binSel,pos,mostCommonSym)
        if len(binSel)==1:
            break
    return binSel[0][0]

def getCo2Rate(binInput):
    binSel = binInput
    wordLength = len(binInput[0][0])
    for pos in range(0,wordLength):
        mostCommonSym = getPrevalentSymbol(binSel, pos, "0")
        if mostCommonSym=="equal":
            leastCommonSym = "0"
        else:
            leastCommonSym = getSymbolNegation(mostCommonSym)
        binSel = selectCompliantWords(binSel,pos,leastCommonSym)
        #print(pos)
        #print(binSel)
        if len(binSel)==1:
            break
    return binSel[0][0]

def countOnes(binInput):
    wordLength = len(binInput[0][0])
    onesCounter = [0]*wordLength
    for line in binInput:
        for i in range(0,wordLength):
            symbol = line[0][i]
            onesCounter[i] += int(symbol=="1")
    return onesCounter

def getPrevalentSymbol(binInput,pos,preferredSymbol="1"):
    numWords = len(binInput)
    onesCounter = 0
    for line in binInput:
        onesCounter += int(line[0][pos]=="1")
    if onesCounter > numWords/2:
        prevalent = "1"
    elif onesCounter < numWords/2:
        prevalent = "0"
    else:
        prevalent = "equal"
    return prevalent

def selectCompliantWords(binInput,pos,symbolSel):
    binSelected = []
    for line in binInput:
        if line[0][pos]==symbolSel:
            binSelected.append([line[0]])
    return binSelected


def getSymbolNegation(symbol):
    return str(int(not bool(int(symbol)))) # Get negation (1->0, 0->1)

def bin2dec(binStr):
    return int(binStr,2)

def getRating(rate1bin,rate2bin):
    return bin2dec(rate1bin)*bin2dec(rate2bin)


if __name__ == "__main__":
    inputPath = "input.txt"
    binInput = loadBinaryInput(inputPath)
    
    rates = getGammaEpsilon(binInput)
    powerConsumption = getRating(*rates)
    print("powerConsumption: "+str(powerConsumption))
    
    oxygenRateBin = getOxygenRate(binInput)
    print("oxygenRate: "+str(bin2dec(oxygenRateBin)))
    co2RateBin = getCo2Rate(binInput)
    print("co2Rate: "+str(bin2dec(co2RateBin)))
    
    lifeSupportRating = getRating(oxygenRateBin,co2RateBin)
    print("lifeSupportRating: "+str(lifeSupportRating))

# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 07:09:40 2021

@author: Martin Kovar
"""

def loadTextfile(path):
    pairingRules = dict()
    with open(path, "r") as file:
        template = file.readline().rstrip()
        file.readline() # Skip empty line
        lines = [line.rstrip() for line in file]   
        for line in lines:
            pair,insertion = line.split(" -> ")
            pairingRules[(pair)] = insertion
    return template,pairingRules

def polymerizeSimple(template,pairingRules,numSteps,printPolLen=False):
    # ... Based on actually building the polymer as a string
    polymer = template
    i = 0
    while i < numSteps:
        polymerUpdated = polymer[0]
        for idx in range(1,len(polymer)):
            pair = polymer[idx-1:idx+1]
            polymerUpdated += pairingRules[pair] + pair[1]
        polymer = polymerUpdated
        i += 1
        if printPolLen:
            print("Polymer length after {} steps: {}".format(i,len(polymer)))
    return polymer

def polymerizeEfficient(template,pairingRules,numSteps):
    # ... Based on counting insertions
    pairsRegister = dict()
    elementsRegister = dict()
    i = 0
    # Initialize pairsRegister:
    for idx in range(1,len(template)):
        pair = template[idx-1:idx+1]
        if pair in pairsRegister:
            pairsRegister[pair] += 1
        else:
            pairsRegister[pair] = 1
    # Count pairs during polymerization:
    while i < numSteps:
        addedPairsRegister = dict()
        for key,value in pairsRegister.items():
            insElem = pairingRules[key]
            insertion = key[0] + pairingRules[key] + key[1]
            newPair1 = insertion[:2]
            newPair2 = insertion[1:]
            # Add number of newly created pairs into the register:
            for p in [newPair1,newPair2]:
                if p in addedPairsRegister:
                    addedPairsRegister[p] += value
                else:
                    addedPairsRegister[p] = value
            # Count new insertions:
            if insElem in elementsRegister:
                elementsRegister[insElem] += value
            else:
                elementsRegister[insElem] = value
        pairsRegister = addedPairsRegister
        i += 1
    # Increment insertions register by characters initially in template:
    for char in template:
        elementsRegister[char] += 1
    return pairsRegister,elementsRegister

def getPolymerScoreFromPolymer(polymer):
    alphabet = set(polymer)
    charCounter = dict()
    # Count all character occurences in polymer
    for char in alphabet:
        charCounter[char] = polymer.count(char)
    return getPolymerScoreFromElemReg(charCounter)

def getPolymerScoreFromElemReg(insertionsRegister):
    mostCommonChar = max(insertionsRegister, key=insertionsRegister.get)
    leastCommonChar = min(insertionsRegister, key=insertionsRegister.get)
    score = insertionsRegister[mostCommonChar] - insertionsRegister[leastCommonChar]
    return score


if __name__ == "__main__":
    inputPath = "input.txt"
    template,pairingRules = loadTextfile(inputPath)
 
    numSteps1 = 10
    polymer = polymerizeSimple(template,pairingRules,numSteps1,printPolLen=True)
    score = getPolymerScoreFromPolymer(polymer)
    print("Polymer score after {} steps, method 1: {}".format(numSteps1,score))
    print("\n")
    
    numSteps2 = 40
    pairsRegister,elementsRegister = polymerizeEfficient(template,pairingRules,numSteps2)
    score2 = getPolymerScoreFromElemReg(elementsRegister)
    print("Polymer score after {} steps, method 2: {}".format(numSteps2,score2))
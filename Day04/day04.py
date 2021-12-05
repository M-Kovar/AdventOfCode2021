# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 08:58:15 2021

@author: mapup
"""

def loadTextfile(path):
    with open(path, "r") as file:
        inputList = [line.rstrip() for line in file]
    return inputList


def processInput(inputList):
    boardIdx = -1
    drawnNumbers = [int(i) for i in inputList.pop(0).split(",")]
    boards = []
    for line in inputList:
        if line=="":
            boardIdx += 1
            boards.append([])
        else:
            lineInt = [int(i) for i in line.split()]
            boards[boardIdx].append(lineInt)
    return drawnNumbers,boards


class BingoGame:
    def __init__(self, bingoBoards):
        self.boards = self.createBoards(bingoBoards)
        self.calledNumbers = []
        self.winningBoardNumber = None
        
    def createBoards(self, bingoBoards):
        boards = []
        boardNum = 0
        for board in bingoBoards:
            boards.append(BingoBoard(board, boardNumber=boardNum))
            boardNum += 1
        return boards
        
    def checkNumber(self, number):
        self.calledNumbers.append(number)
        winResults = []
        winningBoardsIdx = []
        for idx,board in enumerate(self.boards):
            winResult = board.checkNumber(number)
            if winResult:
                print("Board no. {} won! Winning sum is {}. Board removed".format(self.boards[idx].getBoardNumber(),winResult))
                winningBoardsIdx.append(idx)
            winResults.append(winResult)
        self.removeBoards(winningBoardsIdx)
        return winResults
    
    def removeBoards(self,boardsIdx):
        for idx in sorted(boardsIdx, reverse=True):
            del self.boards[idx]
        return
    
    def getWinningBoardNumber(self):
        return self.winningBoardNumber
    
    def getNumberOfBoards(self):
        return len(self.boards)
    
    def printBoards(self):
        for board in self.boards:
            board.printBoard()


class BingoBoard:
    def __init__(self, board, boardNumber=None):
        self.board = board
        self.boardNumber = boardNumber
        self.calledNumbers = []
    
    def checkNumber(self, number):
        self.board = self.markNumber(number)
        winResult = self.checkIfWins()
        return winResult
    
    def markNumber(self, number):
        self.calledNumbers.append(number)
        updatedBoard = self.board
        for row in range(0,len(updatedBoard[0])):
            for col in range(0,len(updatedBoard[row])):
                if updatedBoard[row][col]==number:
                    updatedBoard[row][col] = 0 
        return updatedBoard
    
    def checkIfWins(self):
        boardWins = False
        winResult = None
        # Check rows if won:
        for line in self.board:
            if sum(line)==0:
                boardWins = True
                break
        # Check columns if won:
        for i in range(0,len(self.board[0])):
            if sum(row[i] for row in self.board)==0:
                boardWins = True
                break
        # Calculate win sum, if won:
        if boardWins:
            unmarkedNumSum = sum(sum(self.board,[]))
            winResult = unmarkedNumSum*self.calledNumbers[-1]
        return winResult
    
    def printBoard(self):
        print(self.board)
        return
    
    def getBoardNumber(self):
        return self.boardNumber



if __name__ == "__main__":
    inputPath = "input.txt"
    binInput = loadTextfile(inputPath)
    drawnNumbers,boards = processInput(binInput)
    game = BingoGame(boards)
    
    for i in range(0,len(drawnNumbers)):
        num = drawnNumbers[i]
        print("\nChecking number {}".format(num))
        winResult = game.checkNumber(num)
        if game.getNumberOfBoards()==0:
            print("\nENDING GAME")
            break
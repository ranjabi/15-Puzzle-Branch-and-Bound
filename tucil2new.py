from copy import deepcopy
import read
import time
import random

# Global variable
nodeNumber = 1
depth = 0
path = []

class Elmt:
    def __init__(self, pos):
        self.val = -1
        self.pos = pos

class Puzzle:
    def __init__(self, emptyPos):
        self.name = 1
        self.elmt = [[Elmt( (i+1) + (4*j) ) for i in range(4)] for j in range(4)]
        self.fp = 0
        self.gp = 0
        self.cost = 0
        self.emptyPos = emptyPos
        self.emptyPosRow = (emptyPos-1)//4
        self.emptyPosCol = (emptyPos-1)%4
        self.nextMove = {"up": True, "right": True, "down": True, "left": True}
        self.prevMove = ""
        self.path = []
        
    def elmtToList(self):
        list = [[-1 for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                list[i][j] = self.elmt[i][j].val
        return list
    
        
    def incrNode():
        global nodeNumber
        nodeNumber += 1

    def rowColToPos(self, row, col):
    # convert 4x4 index to 0 index
        return ((row+1) + (4*col))

    def posToRowCol(self, n):
    # convert 1 index to 4x4 index
        row = (n-1)//4
        col = (n-1)%4
        return row, col
            
    def findEmptyMatrix(self, flatten):
    # return empty position
        for i in range(4):
            for j in range(4):
                if self.elmt[i][j].val == -1:
                    if flatten:
                        # 1 index
                        return self.elmt[i][j].pos
                    else:
                        # 4x4 index
                        return self.posToRowCol(self.elmt[i][j].pos)

    def findPos(self, val):
    # return 1 index of val
        pos = -99
        for i in range(4):
            for j in range(4):
                if self.elmt[i][j].val == val:
                    pos = self.elmt[i][j].pos
        if val == 16:
            return 16
        else:
            return pos

    def getKurang(self, iparam):
    # return the number of inversion of iparam
        count = 0
        for i in range(4):
            for j in range(4):
                if (self.elmt[i][j].val < iparam) and (self.elmt[i][j].pos > self.findPos(iparam) and self.elmt[i][j].val != -1):
                    count += 1
        return count
    
    def getKurang16(self):
    #  return the number of inversion of 16 pos
        count = 0
        for i in range(4):
            for j in range(4):
                if (self.elmt[i][j].val < 16) and (self.elmt[i][j].pos > self.findPos(-1) and self.elmt[i][j].val != -1):
                    count += 1
        return count
    
    def isArsirPos(self):
    # return true if empty position on arsir area
        isArsir = False
        if ((self.emptyPos == 2) or (self.emptyPos == 4) or (self.emptyPos == 5) or (self.emptyPos == 7) or (self.emptyPos == 10) or (self.emptyPos == 12) or (self.emptyPos == 13) or (self.emptyPos == 15)):
            return True 
        return isArsir
    
    def getGoal(self):
    # return goal
        x = 0
        sumKurang = 0
        if self.isArsirPos()==True:
            x = 1
        for i in range(1, 16):
            print(i, self.getKurang(i))
            sumKurang += self.getKurang(i)
        lastKurang = self.getKurang16()
        self.goal = (sumKurang+x+lastKurang)
        return (sumKurang+x+lastKurang)
        
    def initCost(self):
    # init new cost
        self.cost = self.fp + self.gp
        
    def printNextMove(self):
    # print next move
        for key in self.nextMove:
            print(key, ":", self.nextMove[key])
        
    def getVal(self, i, j):
    # get val at index i, j
        return self.elmt[i][j].val
    
    def getPos(self, i, j):
    # get pos at index i, j
        return self.elmt[i][j].pos
        
    def posToRow(self, n):
    # convert n on 1 index to row on 0 index
        return ((n-1)//4)
    
    def posToCol(self, n):
    # convert n on 1 index to col on 0 index
        return ((n-1)%4)
    
    def print(self):
    # print current node puzzle
        print("---------" + str(self.name) + "---------")
        for i in range(4):
            for j in range(4):
                if j == 0:
                    print("[", end="")
                
                output = self.elmt[i][j].val
                if len(str(self.elmt[i][j].val)) == 1:
                    output = " " + str(self.elmt[i][j].val)
                print("", output, "", end="")
                if j == 3:
                    print("]", end="")
                if ((j+1) % 4 == 0):
                    print("")
        print("fp:", self.fp)
        print("gp:", self.gp)
        print("cost:", self.cost)
        print("empty pos:", self.emptyPos)
        print("empty pos row:", self.emptyPosRow)
        print("empty pos col:", self.emptyPosCol)
        print("prev move:", self.prevMove)
        self.printNextMove()
        print("===================\n")
        
    def getWrongPos(self):
    # return the number of wrong position
        countWrongPos = 0
        for i in range(4):
            for j in range(4):
                # print(i, j)
                if self.getVal(i,j) != self.getPos(i,j) and self.getVal(i,j) != -1:
                        countWrongPos += 1
        return countWrongPos
        
    def isFinish(self):
    # return true if puzzle is finished
        finish = True
        for i in range(4):
            for j in range(4):
                if self.elmt[i][j].val != self.elmt[i][j].pos and self.getVal(i,j) != -1:
                    return False
        return finish
    
    def findEmpty(self, flatten):
    # return index for empty position
        for i in range(4):
            for j in range(4):
                if self.elmt[i][j].val == -1:
                    if flatten:
                        # 1 index
                        return self.elmt[i][j].pos
                    else:
                        # 4x4 index
                        return self.posToRowCol(self.elmt[i][j].pos)
    
    def move(self, direction):
    # move empty pos to certain direction
        row = self.emptyPosRow
        col = self.emptyPosCol
        moveRow = 0
        moveCol = 0
        if direction=="up":
            moveRow = -1
            moveCol = 0
        if direction=="down":
            moveRow = 1
            moveCol = 0
        if direction=="left":
            moveRow = 0
            moveCol = -1
        if direction=="right":
            moveRow = 0
            moveCol = 1
            
        # exchange empty pos with move position
        self.emptyPos = self.rowColToPos(self.emptyPosRow+moveRow,self.emptyPosCol+moveCol)
        self.emptyPosRow = self.emptyPosRow+moveRow
        self.emptyPosCol = self.emptyPosCol+moveCol
        
        newPos = self.rowColToPos(row+moveRow,col+moveCol)
        emptyRow, emptyCol = self.findEmpty(False)
        
        temp = self.elmt[emptyRow+moveRow][emptyCol+moveCol].val
        self.elmt[emptyRow+moveRow][emptyCol+moveCol].val = -1
        self.elmt[emptyRow][emptyCol].val = temp 
        
    def checkMove(self):
    # check all possible move
        for key in self.nextMove:
            self.nextMove[key] = True
        row, col = self.findEmpty(False)
        if (col == 3 or col == 4):
            self.nextMove["right"] = False 
        if (col == 0):
            self.nextMove["left"] = False 
        if (row == 0):
            self.nextMove["up"] = False 
        if (row == 3 or row == 4):
            self.nextMove["down"] = False
        if self.prevMove != "":
            if self.prevMove == "up":
                self.nextMove["down"] = False
            if self.prevMove == "down":
                self.nextMove["up"] = False
            if self.prevMove == "left":
                self.nextMove["right"] = False
            if self.prevMove == "right":
                self.nextMove["left"] = False

    def __lt__(self, other):
    # overload less than operator for two matrix
        return (self.cost < other.cost) and (self.name < other.name)
    
    def generateNextMove(self, queue):
    # generate next move and add it to queue
        global depth
        global nodeNumber
        global path
        depth += 1
        
        self.checkMove()
        
        for key in self.nextMove:
            if self.nextMove[key] == True:
                temp = deepcopy(self)
                temp.move(key)
                temp.checkMove()
                temp.prevMove = key
                nodeNumber += 1
                temp.name = nodeNumber
                temp.fp += 1
                temp.gp = temp.getWrongPos()
                temp.initCost()
                temp.path.append([key, temp.elmtToList()])
                queue.append((temp.cost, temp))
        queue.sort(reverse=True)

def printQueue(queue):
# print queue
    for i in range(len(queue)):
        print("(cost(as queue key):",queue[i][0],",nodeName:",queue[i][1].name, queue[i][1].prevMove, "parent",queue[i][1].parent)
            

def main(puzzle):
    global depth
    global path
    startTime = time.time()
    depth = 0
    nodeNumber = 0
    
    if (puzzle.goal % 2) != 0:
        print("Puzzle tidak dapat diselesaikan")
    else:
        queue = []
        queue.append((puzzle.cost, puzzle))
        if (puzzle.isFinish()):
            head = queue.pop()
            return puzzle
        while (len(queue) != 0):
            head = queue.pop()
            if head[1].isFinish():
                puzzle.print()
                endTime = time.time()
                print(endTime - startTime)
                print("finish")
                print("node generated:", nodeNumber)
                print(head[1].path)
                # path.reverse()
                path = head[1].path
                for i in range(len(path)):
                    print(path[i][0])
                    for j in range(4):
                        for k in range(4):
                            print(path[i][1][j][k], ",", end="")
                        print()
                return head[1]
            else:
                head[1].generateNextMove(queue)

while True:
    filename = ""
    option = input("Pilih input: ")
    filename = "input" + str(option) + ".txt"
    if option == '0':
        # generate random puzzle
        readPuzzleFlat = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        for i in range(5):
            random.shuffle(readPuzzleFlat)
        for i in range(16):
            if readPuzzleFlat[i] == 16:
                readPuzzleFlat[i] = 'x'
                emptyPos = i+1
        readPuzzle = [[-1 for i in range(4)] for j in range(4)]
        k = 0
        for i in range(4):
            for j in range(4):
                readPuzzle[i][j] = readPuzzleFlat[k]
                k += 1
    else:
        print(filename)
        readPuzzle = read.run(filename)
        
        for i in range(4):
            for j in range(4):
                if readPuzzle[i][j] == 'x':
                    emptyPos = i+1 + 4*j
                
    puzzle = Puzzle(emptyPos)
    
    for i in range(4):
        for j in range(4):
            if readPuzzle[i][j] == 'x':
                puzzle.elmt[i][j].val = -1
                emptyPos = i+1 + 4*j
            else:
                puzzle.elmt[i][j].val = int(readPuzzle[i][j])
                
    print("empty pos", emptyPos)
    
    
    puzzle.emptyPos = puzzle.findEmpty(True)
    print(puzzle.emptyPos)
    print("goal", puzzle.getGoal())
    
    if puzzle.getGoal() % 2 == 0:
        main(puzzle)
    else:
        print("unreachable")
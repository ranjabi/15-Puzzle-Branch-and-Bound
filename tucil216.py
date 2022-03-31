from ctypes.wintypes import LANGID, LARGE_INTEGER
from queue import PriorityQueue
from copy import deepcopy
from telnetlib import DO
import read
import time

class Elmt:
    def __init__(self, pos):
        self.val = -1
        self.pos = pos

nodeNumber = 1
nodeGenerated = 0
depth = 0
path = []
def incrNode():
    global nodeNumber
    nodeNumber += 1

def rowColToPos(row, col):
    return ((row+1) + (4*col))

def posToRowCol(n):
# n 1 index to row col 0 index
    row = (n-1)//4
    col = (n-1)%4
    return row, col

def printPath(curNode):
    global path 
    if (curNode.parent != None):
        path.append([curNode.parent.name, curNode.name, curNode.prevMove])
        printPath(curNode.parent)

class Puzzle:
    def __init__(self):
        self.parent = None
        self.name = 1
        self.elmt = [Elmt(i) for i in range(16)]
        self.fp = 0
        self.gp = 0
        self.cost = 0
        self.goal = 0
        self.child = {}
        self.emptyPos = 7
        self.nextMove = {"up": True, "right": True, "down": True, "left": True}
        self.prevMove = ""

    def findPos(self, val):
    # return 1 indexing of val
        pos = -99
        for i in range(16):
            if self.elmt[i].val == val:
                    pos = self.elmt[i].pos
        if val == 16:
            return 16
        else:
            return pos

    def getKurang(self, iparam):
        count = 0
        for i in range(16):
            if self.elmt[i].val < iparam and self.elmt[i].pos > self.findPos(iparam) and self.elmt[i].val != -1:
                count += 1
        return count
    
    def getKurang16(self, iparam):
        count = 0
        for i in range(16):
            if self.elmt[i].val < 16 and self.elmt[i].pos > self.findPos(iparam) and self.elmt[i].val != -1:
                count += 1
        return count
    
    def isArsirPos(self):
        isArsir = False
        if ((self.emptyPos == 2) or (self.emptyPos == 4) or (self.emptyPos == 5) or (self.emptyPos == 7) or (self.emptyPos == 10) or (self.emptyPos == 12) or (self.emptyPos == 13) or (self.emptyPos == 15)):
            return True 
        return isArsir
    
    def getGoal(self):
        # if genap then reachable
        x = 0
        sumKurang = 0
        # print(self.isArsirPos())
        if self.isArsirPos()==True:
            x = 1
        for i in range(1, 16):
            # print(i, self.getKurang(i))
            sumKurang += self.getKurang(i)
        lastKurang = self.getKurang16(-1)
        self.goal = (sumKurang+x+lastKurang)
        return (sumKurang+x+lastKurang)
        
    def initCost(self):
        self.cost = self.fp + self.gp
        
    def printNextMove(self):
        for key in self.nextMove:
            print(key, ":", self.nextMove[key])
        
    def getVal(self, i, j):
        return self.elmt[i][j].val
    
    def getPos(self, i, j):
        return self.elmt[i][j].pos
        
    def posToRow(self, n):
        # n 1 index to col 0 index
        return ((n-1)//4)
    
    def posToCol(self, n):
        # n 1 index to col 0 index
        return ((n-1)%4)
    
    def printChild(self):
        print("child of:----", self.name, "----------------start>")
        for key in self.child:
            self.child[key].print()
        print("child:--------------------------end>")
    
    def print(self):
        print("---------" + str(self.name) + "---------")
        for i in range(16):
            print(self.elmt[i].val, "," , end="")
        # for i in range(4):
        #     for j in range(4):
        #         if j == 0:
        #             print("[", end="")
                
        #         output = self.elmt[i][j].getVal()
        #         if len(str(self.elmt[i][j].getVal())) == 1:
        #             output = " " + str(self.elmt[i][j].getVal())
        #         print("", output, "", end="")
        #         if j == 3:
        #             print("]", end="")
        #         if ((j+1) % 4 == 0):
        #             print("")
                # print("i:", i, "j:", j)
        print("parent", self.parent)
        print("fp:", self.fp)
        print("gp:", self.gp)
        print("cost:", self.cost)
        print("empty pos:", self.emptyPos)
        print("prev move:", self.prevMove)
        self.printNextMove()
        print("===================\n")
        
    def getWrongPos(self):
    # return wrong position (inversion)
        countWrongPos = 0
        for i in range(16):
            if self.elmt[i].val != -1:
                if self.elmt[i].val != self.elmt[i].pos:
                    countWrongPos += 1
        return countWrongPos
        
    def isFinish(self):
        finish = True
        for i in range(16):
            if self.elmt[i].val != self.elmt[i].pos and self.elmt[i].val != -1:
                return False
        return finish
    
    def findEmpty(self, flatten):
    # return index for -1 (empty box)
        for i in range(16):
            if self.elmt[i].val == -1:
                if flatten:
                    # 1 index
                    return self.elmt[i].getPos()
                # else:
                #     # 4x4
                #     return posToRowCol(self.elmt[i][j].getPos())
            
    
    def move(self, direction):
        if direction=="up":
            nMove = -4
        elif direction=="down":
            nMove = +4
        elif direction=="left":
            nMove = -1
        elif direction=="right":
            nMove = +1
        
        # 0 index
        idxEmptyPos = self.emptyPos-1
        temp = self.elmt[idxEmptyPos+nMove]
        
        self.elmt[idxEmptyPos] = temp
        
        self.emptyPos = self.emptyPos + nMove
        self.elmt[idxEmptyPos].val = -1
        self.elmt[idxEmptyPos].pos = self.emptyPos+1
        

        
        
    def checkMove(self):
        for key in self.nextMove:
            self.nextMove[key] = True
        pos = self.emptyPos
        if (pos % 4 == 0):
            self.nextMove["right"] = False 
        if (pos % 4 == 1):
            self.nextMove["left"] = False 
        if (pos == 1 or pos == 2 or pos == 3 or pos == 4):
            self.nextMove["up"] = False 
        if (pos == 13 or pos == 14 or pos == 15 or pos == 16):
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
        # (self.name < other.name) and 
        return (self.cost < other.cost) and (self.name > other.name)
    # def __gt__(self, other):
    #     # (self.name < other.name) and 
    #     return (self.cost < other.cost) and (self.name > other.name)
    # def __le__(self, other):
    #     return (self.cost < other.cost) or (self.cost == other.cost)
        
    def getSmallestChildCost(self):
        minKey = next(iter(self.child))
        for key in self.child:
            if self.child[key] < self.child[minKey]:
                minKey = key
        return minKey
    
    def generateNextMove(self, queue):
        global depth
        depth += 1
        # print(depth)
        global nodeGenerated
        # print("next move is generated ===========================")
        global nodeNumber
        global path
        self.checkMove()
        for key in self.nextMove:
            if self.nextMove[key] == True:
                temp = deepcopy(self)
                temp.parent = self
                temp.move(key)
                temp.prevMove = key
                incrNode()
                temp.name = nodeNumber
                temp.fp += 1
                temp.gp = temp.getWrongPos()
                temp.initCost()
                # print("================================temp cost:", temp.cost)
                nodeGenerated += 1
                
                self.child.update({temp.name:temp})
        # smallestKey = self.getSmallestChildCost()
        # smallest = self.child[smallestKey]
        # queue.append((smallest.cost, smallest))
                queue.append((temp.cost, temp))
                queue.sort(reverse=True)

p1 = Puzzle()
# p1.elmt[0][0].val = 1
# p1.elmt[0][1].val = 2
# p1.elmt[0][2].val = 3
# p1.elmt[0][3].val = 4
# p1.elmt[1][0].val = 5
# p1.elmt[1][1].val = 6
# # p1.elmt[1][2].val = 1
# p1.elmt[1][3].val = 8
# p1.elmt[2][0].val = 9
# p1.elmt[2][1].val = 10
# p1.elmt[2][2].val = 7
# p1.elmt[2][3].val = 11
# p1.elmt[3][0].val = 13
# p1.elmt[3][1].val = 14
# p1.elmt[3][2].val = 15
# p1.elmt[3][3].val = 12

def printQueue(queue):
    for i in range(len(queue)):
    # for i in range(len(queue.queue)):
        print("(cost(as queue key):",queue[i][0],",nodeName:",queue[i][1].name, queue[i][1].prevMove, "parent",queue[i][1].parent)

# def minimizeQueue(queue):
#     head = queue.get()
#     smallest = head[1].cost
#     queue.put(head[1].cost,head[1])
#     for i in range(queue.qsize()):
#         if queue.queue[0] > smallest:
            

def asd(puzzle):
    startTime = time.time()
    global depth
    global path
    # if (puzzle.goal % 2) == 0:
    singleOccurance = False
    queue = []
    queue.append((p1.cost, p1))
    # puzzle.print()
    if (p1.isFinish()):
        # printQueue(queue)
        t = queue.get()
        # t[1].print()
        return p1
    while (len(queue) != 0):
        # if startTime > startTime + 5:
        # if depth == 1:
        #     head = queue.pop()
        #     print("node generated:", nodeGenerated)
        #     printPath(head[1])
        #     path.reverse()
        #     print(path)
        #     break
        
        # if depth == 5:
        #     print("node generated:", nodeGenerated)
        # # if head[1].fp == 10:
        # #     head = queue.pop()
        # #     head[1].print()
        # # #     printQueue(queue)
        # #     print(move)
        #     break
        head = queue.pop()
        
        # printQueue(queue)
        # head[1].print()
        if head[1].isFinish():
            # head[1].print()
            endTime = time.time()
            print(endTime - startTime)
            print("finish")
            print("node generated:", nodeGenerated)
            printPath(head[1])
            path.reverse()
            print(path)
            return head[1]
        else:
            # print(depth)
            # printQueue(queue)
            head[1].generateNextMove(queue)

    # else:
    #     print("unreachable")
    

# asd(p1)
# print(p1.elmt)

def readFile():
    readPuzzle = read.run("input1.txt")
    for i in range(16):
            if readPuzzle[i] == 'x':
                p1.elmt[i].val = -1
            else:
                p1.elmt[i].val = int(readPuzzle[i])
    

    # p1.emptyPos = p1.findEmpty(True)
    # print(p1.emptyPos)
    # for i in range(4):
    #     for j in range(4):
    #         # print(i, j)
    #         print(p1.elmt[i][j].val)
# for i in range(4):
#     for j in range(4):
#         # print(i, j)
#         print("manual input", p1.elmt[i][j].val)
readFile()
p1.emptyPos = p1.findPos(-1)
print(p1.emptyPos)
print("goal", p1.getGoal())
# p1.print()
# print(p1.getWrongPos())
asd(p1)

# @ TO DO: FIX LOGIC GENERATE NEXT MOVE
# 
# @@ TO DO
# - MEKANISME QUEUE
# - ada child yang seharusnya engga ada 
# @@ TO DO:
# - SELAMA MASIH DI SUATU CHILD JANGAN PINDAH KE CHILD YANG LAIN 
# - MODIF PRIOQUEUE BIAR TAU MANA YANG DIAKSES BIAR GA PINDAH"



    
def run(filename):
    f = open(filename, "r")
    # print(f.readlines())
    list = [-99 for i in range(16)]
    j = 0
    for x in f:
        # print(x.split(), end="")
        # print("line",line)
        for y in x.split():
        # for every number
            # print("col",col)
            list[j] = y
            # print(y)
            j+= 1
        

    # print()
    return list
    
if __name__ == "__main__":
    run()
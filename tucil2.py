from copy import deepcopy
count = 1

# class Puzzle:
#     class Elmt:
#         def __init__(self):
#             self.val = -1
#             self.pos = -1
    
#     def __init__(self):
#         self.Elmt[16]
#         # self.Elmt = [-1 for i in range(16)]
#     def print(self):
#         for i in range(16):
#             if (i % 4 == 0):
#                 print("")
#             if len(str(self.Elmt[i]).val) == 1:
#                 output = " " + str(self.Elmt[i].val)
#             else:
#                 output = str(self.Elmt[i].val) 
#             if (i % 4 == 0):
#                 print("[" + output + " ", end="")
#             elif (i % 4 != 3):
#                 print(output + " ", end="")
#             else:
#                 print(output + "]", end="")
# p1 = Puzzle()
# # print("asd")
# p1.Elmt[0].val = 1
# p1.Elmt[1].val = 2
# p1.Elmt[2].val = 3
# p1.Elmt[3].val = 4
# p1.Elmt[4].val = 5
# p1.Elmt[5].val = 6
# # p1.Elmt[3][2] = 1
# p1.Elmt[7].val = 8
# p1.Elmt[8].val = 9
# p1.Elmt[9].val = 10
# p1.Elmt[10].val = 7
# p1.Elmt[11].val = 11
# p1.Elmt[12].val = 13
# p1.Elmt[13].val = 14
# p1.Elmt[14].val = 15
# p1.Elmt[15].val = 12
# p1.print()
# # list1 = []

# # f = open("input.txt", "r")
# # for x in f:
# #     # print("[" + x + "]")
# #     y = x.split()
# #     print(y)
# #     # print("len:" + str(len(y)))
# #     # # if (len(y) == 3):
# #     # num = str(len(y))
# #     # for z in range(len(y)):
# #     #     p1.Elmt[z] = y[z]
# # # print(list1)

class Elmt:
    def __init__(self, pos):
        self.val = -1
        self.pos = pos
        
    def getVal(self):
        return self.val
    
    def getPos(self):
        return self.pos
    
def posToRowCol(n):
# n 1 index to row col 0 index
    row = (n-1)//4
    col = (n-1)%4
    return row, col

def rowColToPos(row, col):
    return ((row+1) + (4*col))

def newEmptyPos(n, direction):
    row, col = posToRowCol(n)
    if direction=="up":
        return rowColToPos(row-1,col)
    elif direction=="down":
        return rowColToPos(row+1,col)
    elif direction=="left":
        return rowColToPos(row,col-1)
    elif direction=="right":
        return rowColToPos(row,col+1)
    
nodeNumber = 1

def incrNode():
    global nodeNumber
    nodeNumber += 1
    
class PriorityQueue(object):
    def __init__(self):
        self.queue = []
  
    def __str__(self):
        return ' '.join([str(i) for i in self.queue])
  
    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0
  
    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)
  
    # for popping an element based on Priority
    def delete(self):
        try:
            max = 0
            for i in range(len(self.queue)):
                if self.queue[i].cost > self.queue[max].cost:
                    max = i
            item = self.queue[max].nodeNumber
            del self.queue[max]
            return item
        except IndexError:
            print()
            exit()
    
class Puzzle:
    
    def __init__(self):
        # for i in range(16):
        self.nodeNumber = 1
        self.elmt = [[Elmt( (i+1) + (4*j) ) for i in range(4)] for j in range(4)]
        self.emptyPos = 6
        self.fp = 1
        self.gp = 0
        self.cost = self.fp + self.gp
        self.nextMove = {"up": True, "down": True, "left": True, "right": True}
        self.child = {}
        
    def setGP(self):
    # count gp after move is taken
        count = 0
        for i in range(4):
            for j in range(4):
                if self.elmt[i][j].getPos() != self.elmt[i][j].getVal() and self.elmt[i][j].getVal() != -1:
                    count += 1
        self.gp = count
        self.cost = self.fp + 1 + self.gp
        
    def isFinish(self):
        finish = False
        for i in range(4):
            for j in range(4):
                if self.elmt[i][j].getVal() == self.elmt[i][j].getPos():
                    return True
        return finish
        
    def findEmpty(self):
    # return 0 index of row and col for -1 (empty box)
        for i in range(4):
            for j in range(4):
                if self.elmt[i][j].getVal() == -1:
                    return posToRowCol(self.elmt[i][j].getPos())
               
    def print(self):
        for i in range(4):
            for j in range(4):
                if j == 0:
                    print("[", end="")
                
                output = self.elmt[i][j].getVal()
                if len(str(self.elmt[i][j].getVal())) == 1:
                    output = " " + str(self.elmt[i][j].getVal())
                print("", output, "", end="")
                if j == 3:
                    print("]", end="")
                if ((j+1) % 4 == 0):
                    print("")
                # print("i:", i, "j:", j)
        print("fp:", self.fp)
        print("gp:", self.gp)
        print("cost:", self.cost)
        for key in self.nextMove:
            print(key, self.nextMove[key])
        print("-------------------")
                
                
    def getWrongPos(self):
        countWrongPos = 0
        for i in range(4):
            for j in range(4):
                if self.elmt[j].getVal() != -1:
                    if self.val != self.pos:
                        countWrongPos += 1
    
    def generateNextMove(self, queue):
    # add child puzzle
        row, col = posToRowCol(self.emptyPos)
        if (col == 3):
            self.nextMove["right"] = False 
        if (col == 0):
            self.nextMove["left"] = False 
        if (row == 0):
            self.nextMove["up"] = False 
        if (row == 3):
            self.nextMove["down"] = False
    
        for key in self.nextMove:
            temp = deepcopy(self) 
            print("temp.fp", temp.fp)

            if self.nextMove[key] == True:
                print(key)
                if key=="isUp":
                    temp.move("up")
                elif key=="isDown":
                    temp.move("down")
                elif key=="isLeft":
                    temp.move("left")
                elif key=="isRight":
                    temp.move("right")
                incrNode()
                temp.setGP()
                temp.nodeNumber = nodeNumber
                print("nodenumber:", nodeNumber)
                queue.insert(temp)
                self.child.update({nodeNumber:temp})
                
    def findPos(self, val):
    # return 1 indexing of val
        pos = -99
        for i in range(4):
            for j in range(4):
                if self.elmt[i][j].getVal() == val:
                    pos = self.elmt[i][j].getPos()
        return pos
                
    def getKurang(self, iparam):
        iPos = self.findPos(iparam)
        print(iPos)
        count = 0
        for i in range(4):
            for j in range(4):
                # if (self.elmt[param].getPos() > ((i+1) + (4*j))) and self.elmt[param].getValue() < self.elmt[i][j]:
                if (self.elmt[i][j].getVal() < iparam) and (self.elmt[i][j].getPos() > self.findPos(iparam) and self.elmt[i][j].getVal() != -1):
                    count += 1
                    # posisi lebih dari param tapi valuenya kurang dari param
        return count
    
    def move(self, direction):
        row, col = posToRowCol(self.emptyPos)
        if direction=="up":
            moveRow = (-1)
            moveCol = 0
            
        elif direction=="down":
            moveRow = 1
            moveCol = 0
        elif direction=="left":
            moveRow = 0
            moveCol = -1
        elif direction=="right":
            moveRow = 0
            moveCol = 1
            
        newPos = rowColToPos(row+moveRow,col+moveCol)
        emptyRow, emptyCol = self.findEmpty()
        
        # top/bottom/left/right empty elmt
        temp = self.elmt[emptyRow+moveRow][emptyCol+moveCol].getVal()
        self.elmt[emptyRow+moveRow][emptyCol+moveCol].val = -1
        self.elmt[emptyRow][emptyCol].val = temp
            
def cost(puzzle):
    puzzle.fp + puzzle.getWrongPos()
            
p1 = Puzzle()
p1.elmt[0][0].val = 1
p1.elmt[0][1].val = 2
p1.elmt[0][2].val = 3
p1.elmt[0][3].val = 4
p1.elmt[1][0].val = 5
p1.elmt[1][1].val = 6
# p1.elmt[1][2].val = 1
p1.elmt[1][3].val = 8
p1.elmt[2][0].val = 9
p1.elmt[2][1].val = 10
p1.elmt[2][2].val = 7
p1.elmt[2][3].val = 11
p1.elmt[3][0].val = 13
p1.elmt[3][1].val = 14
p1.elmt[3][2].val = 15
p1.elmt[3][3].val = 12

p1.print()


# for i in range(len(p1.child)):
#     print("child:")
#     p1.child[i].print()

myQueue = PriorityQueue()
p1.generateNextMove(myQueue)

print("queue:")
# while not myQueue.isEmpty():
#         print(myQueue.delete()) 


print("---------iterasi pertama:-----------")
print(p1.child)
for key in p1.child:
    print(key)
    p1.child[key].print()
# p1.child[3].print()
# print("---------iterasi kedua:-----------")
# p1.child[3].generateNextMove()
# print(p1.child[3].child)
# for key in p1.child[3].child:
#     print(key)
#     p1.child[3].child[key].print()
# print("---------iterasi ketiga:-----------")
# p1.child[3].child[8].generateNextMove()
# print(p1.child[3].child[8].child)
# for key in p1.child[3].child[8].child:
#     print(key)
#     p1.child[3].child[8].child[key].print()

# @@ TO DO 
# - LINE 168 ADA LINE YANG TIDAK DIINGINKAN
# - PRINT NEXT MOVE MUNGKIN GAPERLU HANYA LIAT KEY NEXTMOVE YANG FALSE AJA, TAPI TAMBAHIN FUNGSI ISBOUND DI GENERATENEXTMOVE
# - BIKIN PAKE PRIOQUEUE
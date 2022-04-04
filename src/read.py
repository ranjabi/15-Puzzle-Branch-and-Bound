def run(filename):
    f = open(filename, "r")
    list = [[0 for i in range(4)] for j in range(4)]
    line = 0
    col = 0
    for x in f:
        col = 0
        for y in x.split():
            list[line][col] = y
            col+= 1
            if (col == 4):
                break
        line += 1
        
    return list
    
if __name__ == "__main__":
    run()
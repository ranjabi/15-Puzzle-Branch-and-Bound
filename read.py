
    
def run(filename):
    f = open(filename, "r")
    # print(f.readlines())
    list = [[0 for i in range(4)] for j in range(4)]
    line = 0
    col = 0
    for x in f:
        # print(x.split(), end="")
        col = 0
        # print("line",line)
        for y in x.split():
        # for every number
            # print("col",col)
            list[line][col] = y
            # print(y)
            col+= 1
            if (col == 4):
                break
        line += 1
        

    # print()
    # print(list)
    return list
    
if __name__ == "__main__":
    run()
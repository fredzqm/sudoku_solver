import sys
import copy
import queue

FULLSET = set([1, 2, 3, 4, 5, 6, 7, 8, 9]);
EMPTY = 0

class sudoku:
    def __init__(self, givenData):
        self.found = [[0]*9 for i in range(9)]   # store the current reached configuration
        self.hori = [FULLSET.copy() for i in range(9)]
        self.vert = [FULLSET.copy() for i in range(9)]
        self.squa = [FULLSET.copy() for i in range(9)]

        for i in range(0 , 9):
            for j in range(0 , 9):
                if givenData[i][j] != EMPTY:
                    self.setValue(i, j, givenData[i][j])
                
    def setValue(self, i, j, n):
        self.found[i][j] = n;
        self.hori[i].remove(n);
        self.vert[j].remove(n);
        self.squa[i//3*3+j//3].remove(n);

    def getPosible(self, i, j):
        return self.hori[i] & self.vert[j] & self.squa[i//3*3+j//3];

    def solve(self):
        changed = True
        while(changed):
            changed = False
            minPos = FULLSET
            for i in range(0 , 9):
                for j in range(0 , 9):
                    if self.found[i][j] == EMPTY:
                        pos = self.getPosible(i, j)
                        if (len(pos) == 0):
                            return None
                        elif (len(pos) == 1):
                            self.setValue(i, j, pos.pop())
                            changed = True
                        else:
                            if len(pos) < len(minPos):
                                minPos, mini, minj = pos, i, j
        
        # return if all positions are filled
        if minPos == FULLSET:
            return self;

        # start backtracking
        for x in minPos:
            nextSudoku = copy.deepcopy(self)
            nextSudoku.setValue(mini, minj, x)
            sol = nextSudoku.solve()
            if sol != None:
                return sol
        
        # None solution is found, all possibilities are examined, impossible to solve    
        return None
    
    
    def checkValid(self):
    # check whether we get a valid solution of the sudoku problem
        for i in range(0, 9):
            x = [False] * 9
            for t in range(0, 9):
                x[self.found[i][t] - 1] = True
            for t in range(0 , 9):
                if x[t] == False:
                    return 'row' , i , t + 1
        
        for i in range(0, 9):
            x = [False] * 9
            for t in range(0, 9):
                x[self.found[t][i] - 1] = True
            for t in range(0 , 9):
                if x[t] == False:
                    return 'col' , i , t + 1
                
        for i in range(0, 9):
            x = [False] * 9
            m , n = (i % 3) * 3 , (i // 3) * 3
            for t in range(0, 9):
                x[self.found[m + t % 3][ n + t // 3] - 1] = True
            for t in range(0 , 9):
                if x[t] == False:
                    return 'sqr' , m , n , t + 1
        return 'Pass'

    def __repr__(self):
        return "\n".join(["".join([str(i) for i in line]) for line in self.found])
    

# use this program by running python sudoku.py file.txt
# file.txt containst the 9x9 configuration of a sudoku game.
# eg:    python sudoku.py sudoku_hardest.txt
if __name__ == "__main__":
    args = sys.argv
    filename = sys.argv[1]
    reader = open(filename , 'r')
    lines = reader.readlines()
    initialData = [[int(line[i]) for i in range(9)] for line in lines]
    
    try:
        game = sudoku(initialData)
    except KeyError:
        print("initial state is not valid!")
        exit(0)
    print("start game:")
    print(game)
    print()
    sol = game.solve()
    print("Solution:")
    print(sol)
    print()
    if sol == None:
        print("No solution exit")
    else:
        print(sol.checkValid())

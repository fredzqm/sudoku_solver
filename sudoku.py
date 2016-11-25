import sys
from Queue import PriorityQueue

class sudoku:
    def __init__(self, givenData):
        self.given = givenData  # store start configuration
        self.found = []  # store the current reached configuration
        self.possibles = []  # store the list of possibilities in each position
        for i in range(0 , 9):
            self.found.append([])
            self.possibles.append([])
            for j in range(0 , 9):
                self.found[i].append(self.given[i][j])
                if self.given[i][j] == 0:
                    self.possibles[i].append(set([1, 2, 3, 4, 5, 6, 7, 8, 9]))
                else:
                    self.possibles[i].append(set([self.given[i][j]]))
    
    def solve(self):
        changed = True
        while(changed):
            changed = False
            # check if there is any conflict and rule out those possibilities that lead to contradiction
            for i in range(0 , 9):
                for j in range(0 , 9):
                    num = self.found[i][j]
                    if num != 0:
                        m , n = (i // 3) * 3 , (j // 3) * 3
                        for t in range(0 , 9):
                            if t != j and num in self.possibles[i][t]:
                                if num == self.found[i][t]:
                                    return None 
                                else:
                                    self.possibles[i][t].remove(num)
                            
                            if t != i and num in self.possibles[t][j]:
                                if num == self.found[t][j]:
                                    return None
                                else:
                                    self.possibles[t][j].remove(num)
                            
                            mx = m + t % 3
                            ny = n + t // 3
                            if (mx != i and ny != j) and num in self.possibles[mx][ny]:
                                if num == self.found[mx][ny]:
                                    return None
                                else:
                                    self.possibles[mx][ny].remove(num)
            # Examine each digit for each row, column and square, and simplify problem based on 
            # the rule that there has to be at least each digit in each row, column and ssquare
            for num in range(1 , 10):
                for i in range(0 , 9):
                    pt = []
                    ct = 0
                    # check for the row
                    for k in range(0 , 9):
                        if num in self.possibles[k][i] :
                            if self.found[k][i] == num:
                                ct = 0
                                break
                            else:
                                ct += 1
                                pt.append((k , i))
                    if ct == 1:
                        changed = True
                        self.found[pt[0][0]][pt[0][1]] = num
                        self.possibles[pt[0][0]][pt[0][1]] = set([num])
                    elif ct > 1:
                        r = pt[0][0] // 3
                        for p in pt:
                            if r != p[0] // 3:
                                r = -1
                                break
                        if r >= 0:
                            m = r * 3
                            n = (i // 3) * 3
                            for t in range(0 , 9):
                                mx = m + t % 3
                                ny = n + t // 3
                                if ny != i and num in self.possibles[mx][ny]:
                                    if self.found[mx][ny] == num:
                                        return None
                                    self.possibles[mx][ny].remove(num)
                    
                    pt = []
                    ct = 0
                    # check for the column
                    for k in range(0 , 9):
                        if num in self.possibles[i][k]:
                            if self.found[i][k] == num:
                                ct = 0
                                break
                            else:
                                ct += 1
                                pt.append((i , k))
                    if ct == 1:
                        changed = True
                        self.found[pt[0][0]][pt[0][1]] = num
                        self.possibles[pt[0][0]][pt[0][1]] = set([num])
                    elif ct > 1:
                        c = pt[0][1] // 3
                        for p in pt:
                            if c != p[1] // 3:
                                c = -1
                                break
                        if c > 0:
                            m = (i // 3) * 3
                            n = c * 3
                            for t in range(0 , 9):
                                mx = m + t % 3
                                ny = n + t // 3
                                if mx != i and num in self.possibles[mx][ny]:
                                    if self.found[mx][ny] == num:
                                        return None
                                    self.possibles[mx][ny].remove(num)
                                        
                    pt = []
                    ct = 0
                    # check for the square
                    m , n = (i % 3) * 3 , (i // 3) * 3
                    for k in range(0 , 9):
                        mx = m + (k % 3)
                        ny = n + (k // 3)
                        if num in self.possibles[mx][ny] :
                            if  self.found[mx][ny] == num:
                                ct = 0
                                break
                            else:
                                ct += 1
                                pt.append((mx , ny))
                    if ct == 1:
                        changed = True
                        self.found[pt[0][0]][pt[0][1]] = num
                        self.possibles[pt[0][0]][pt[0][1]] = set([num])
                    elif ct > 1:
                        r = pt[0][0]
                        for p in pt:
                            if r != p[0]:
                                r = -1
                                break
                        if r >= 0:
                            n = i // 3
                            for t in range(0 , 9):
                                if t // 3 != n and num in self.possibles[r][t]:
                                    if self.found[r][t] == num:
                                        return None 
                                    self.possibles[r][t].remove(num)
                        c = pt[0][1]
                        for p in pt:
                            if c != p[1]:
                                c = -1
                                break
                        if c >= 0:
                            m = i % 3
                            for t in range(0 , 9):
                                if t // 3 != m and num in self.possibles[t][c]:
                                    if self.found[t][c] == num:
                                        return None 
                                    self.possibles[t][c].remove(num)
            # collect those positions with only one possibility                    
            for i in range(0 , 9):
                for j in range(0 , 9):
                    if self.found[i][j] == 0 and len(self.possibles[i][j]) <= 1:
                        if len(self.possibles[i][j]) < 1:
                            return None
                        changed = True
                        num = list(self.possibles[i][j])[0]
                        self.found[i][j] = num
                        self.possibles[i][j] = set([num])
            
        # to choose the position with least variation, most involvement to start backtracking
        minLen = 10
        maxInvol = 0
        pos = None
        for i in range(0 , 9):
            for j in range(0 , 9):
                l = len(self.possibles[i][j])
                if l > 1 and l <= minLen:
                    invol = 0 
                    m , n = (i // 3) * 3 , (j // 3) * 3
                    for t in range(0 , 9):
                        if t != j and num in self.possibles[i][t]:
                            if 0 == self.found[i][t]:
                                invol += 1
                        if t != i and num in self.possibles[t][j]:
                            if 0 == self.found[t][j]:
                                invol += 1
                        mx = m + t % 3
                        ny = n + t // 3
                        if (mx != i and ny != j) and num in self.possibles[mx][ny]:
                            if 0 == self.found[mx][ny]:
                                invol += 1
                    if l < minLen or invol > maxInvol :
                        l = minLen
                        maxInvol = invol
                        pos = (i , j)
        if pos == None:
            return self
        
        # order choices in PQ according to the constraining value
        quene = PriorityQueue()
        for choice in self.possibles[pos[0]][pos[1]]:
            m , n = (i // 3) * 3 , (j // 3) * 3
            invol = 0
            for t in range(0 , 9):
                if t != j and num in self.possibles[i][t]:
                    if choice in self.possibles[i][t]:
                        invol += 1
                if t != i and num in self.possibles[t][j]:
                    if choice in self.possibles[t][j]:
                        invol += 1
                mx = m + t % 3
                ny = n + t // 3
                if (mx != i and ny != j) and num in self.possibles[mx][ny]:
                    if choice in self.possibles[mx][ny]:
                        invol += 1
            quene.put((invol , choice))
            
        # start backtracking
        while quene.qsize() > 0:
            choice = quene.get()[1]
            nextSudoku = sudoku(self.found)
            nextSudoku.found[pos[0]][pos[1]] = choice
            nextSudoku.possibles[pos[0]][pos[1]] = set([choice])
#             nextSudoku.level = self.level + 1
#             print 'Level:  ' + str(self.level)
#             print nextSudoku
            sol = nextSudoku.solve()
            if sol != None:
                return sol
        
        # None solution is found, all possibilities are examined, impossible to solve    
        return None
    
    
    def check(self):
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
        s = ""
        for j in range(0 , 9):
            for i in range(0 , 9):
                s += str(self.possibles[j][i])
            s += '\n'
        return s
    
    def __str__(self):
        s = ''
        for i in range(0 , 9):
            for j in range(0 , 9):
                s += str(self.found[i][j]) 
            s += '\n'
        return s
    
    
# use this program by running python sudoku.py file.txt
# file.txt containst the 9x9 configuration of a sudoku game.
# eg:    python sudoku.py sudoku_hardest.txt
if __name__ == "__main__":
    args = sys.argv
    filename = sys.argv[1]
    reader = open(filename , 'r')
    lines = reader.readlines()
    initialData = []
    for j in range(0 , 9):
        line = lines[j]
        row = []
        for i in range(0, 9):
            row.append(int(line[i]))
        initialData.append(row)
    
    game = sudoku(initialData)
#     game.level = 1
    print "start game:"
    print game
    sol = game.solve()
    print "Solution:"
    print sol
    if sol == None:
        print "No solution exit"
    else:
        print sol.check()

import random

#a class building a classic sudoku,  either 9x9 or 16x16 
#TODO: Find algorithm for 16x16
class Classic_Sudoku:
    #constructor of the sudoku grid
    def __init__(self, monster = False):
        if monster:
            self.subgrid_size = 4
            self.size =  16
        else:
            self.subgrid_size = 3
            self.size =  9
        self.grid = []
        self.characters = []
        for i in range(0,self.size):
            self.characters.append(i+1)
            self.grid.append([0] * self.size)
        self.CSP_filler()
        


    def valid_position(self,  c, x, y):
        #check the provided x and y coordinates
        if x > (self.size - 1) or x < 0:
            raise ValueError(f"X value {x} is out of bounds 0 and {self.size - 1}.")
        if y > (self.size - 1) or y < 0:
            raise ValueError(f"Y value {y} is out of bounds 0 and {self.size - 1}.")
        if c not in self.characters:
            raise ValueError(f"{c} is not part of {self.characters}!!!")

        #check rows and columns
        for i in range(0, self.size):
            if self.grid[x][i]  == c or self.grid[i][y]  == c:
                return False

        #check the subgrid   
        x_start = x - (x%self.subgrid_size)
        x_end = x_start +self.subgrid_size
        y_start = y - (y%self.subgrid_size)
        y_end = y_start + self.subgrid_size    
        for xi in range(x_start, x_end):
            for yi in range(y_start, y_end):
                if self.grid[xi][yi] == c:
                    return False

        return True
        

    def get_free_position(self):

        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.grid[i][j] == 0:
                    return [i,j]

        return []


    def backtracking_filler(self):
        pos = self.get_free_position()
        if pos == []:
            return True
        #shuffle the character list for randomness 
        random.shuffle(self.characters)
        for c in self.characters:
            if self.valid_position(c, pos[0], pos[1]):
                #temporarly assign c to the pos on board 
                self.grid[pos[0]][pos[1]] = c
                #check if c may occupy pos
                if self.backtracking_filler():
                    return True
                self.grid[pos[0]][pos[1]] = 0

        #no valid character has been found the position, backtracking needed
        return False




    def minimum_options(self):
        min =  self.size + 1
        minimal_position = []
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.grid[i][j] != 0:
                    continue
                c = 0
                for ch in self.characters:
                    if self.valid_position(ch,  i, j):
                        c+=1
                if c < min:
                    minimal_position = [(i, j)]
                    min = c
                elif c == min:
                    minimal_position.append((i,j))
        return random.choice(minimal_position)

    def least_constraining_value(self, x, y):
        best_chars = []
        restrictions = 1000
        if self.grid[x][y] != 0:
            return -1
        for c in self.characters:
            if self.valid_position(c, x, y):
                restrictions_c = 0
                self.grid[x][y] = c
                for i in range(0, self.size):
                    if self.grid[i][y] == 0:
                        for ch in self.characters:
                            if self.valid_position(ch, i, y) == False:
                                restrictions_c+=1
                    if self.grid[x][i] == 0:
                        for ch in self.characters:
                            if self.valid_position(ch, x, i) == False:
                                restrictions_c+=1


                x_start = x - (x%self.subgrid_size)
                x_end = x_start +self.subgrid_size
                y_start = y - (y%self.subgrid_size)
                y_end = y_start + self.subgrid_size

                for xi in range(x_start, x_end):
                    if xi == x:
                        continue
                    for yi in range(y_start, y_end):
                        if yi == y or self.grid[xi][yi]:
                            continue
                        for ch in self.characters:
                            if self.valid_position(ch, xi, yi) == False:
                                restrictions_c+=1

                if restrictions_c < restrictions:
                    best_chars = [c]
                    restrictions = restrictions_c
                elif restrictions_c == restrictions:
                    best_chars.append(c)      
                self.grid[x][y] = 0

        #no valid characters have been found
        if best_chars == []:
            return -1
        return random.choice(best_chars)
    
    #fill in the sudoku board using CSP
    def CSP_filler(self):
        empty = (self.size * self.size)
        while empty > 0:
            pos = self.minimum_options()

            charc = self.least_constraining_value(pos[0], pos[1])
            self.grid[pos[0]][pos[1]] = charc
            empty-=1


    #represent the sudoku grid as a string
    def __str__(self):
        sdk = ""
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.grid[i][j] == 10:
                    sdk+= " A |"
                elif self.grid[i][j] == 11:
                    sdk+= " B |"
                elif self.grid[i][j] == 12:
                    sdk+= " C |"
                elif self.grid[i][j] == 13:
                    sdk+= " D |"
                elif self.grid[i][j] == 14:
                    sdk+= " E |"
                elif self.grid[i][j] == 15:
                    sdk+= " F |"
                elif self.grid[i][j] == 16:
                    sdk+= " G |"
                else:
                    sdk+= f" {self.grid[i][j]} |"
            sdk += "\n"
        return sdk


#Testing

# Monster Sudoku
print("Standard Sudoku:")
monster_sudoku = Classic_Sudoku(monster=True)
print(monster_sudoku)

class KillerSufdoku(Classic_Sudoku):
    def __init__(self, subgrid_size):
        super().__init__(subgrid_size)
        self.cages =  []

    #TODO: Implement cages
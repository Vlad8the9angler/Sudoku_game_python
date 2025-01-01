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
        self.undiscovered = []
        self.prepare_board(20)
        


    def valid_position(self,  c:int, x:int, y:int):
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

    def least_constraining_value(self, x:int, y:int):
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
    #prepare the sudoku board to be used 
    def prepare_board(self, pairs):
        #pairs of points to be hidden for the player
        p = pairs
        while p > 0:
            x = random.randint(0, self.size-1)
            y = random.randint(0, self.size-1)
            while (x,y) in self.undiscovered:
                x = random.randint(0, self.size-1)
                y = random.randint(0, self.size-1)
            self.undiscovered.append((x,y))
            self.undiscovered.append(((self.size - 1) - x,(self.size - 1) -y))
            p-=1
    #represent the sudoku grid as a string
    def __str__(self):
        sdk = ""
        for i in range(0, self.size):
            for j in range(0, self.size):
                if (i,j) not in self.undiscovered:
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
                else:
                    sdk+= "   |"
            sdk += "\n"
        return sdk




#class meant to describe cages for killer sudoku
class Cage:
    def __init__(self, positions):
        #positions is an array of x,  y coordinates and the value of the sudoku grid at position x y
        self.positions = positions
        self.size = len(positions)
        self.sum = sum([z for x,y,z in self.positions])

    def __str__(self):
        s  = f"Sum:{self.sum}"
        s+= f"\tLength:{self.size}"
        s+= f"\t{self.positions}"
        return s


class KillerSudoku(Classic_Sudoku):
    def __init__(self, monster:bool = False):
        super().__init__(monster)
        self.cages =  []
        #create 
        self.free_positions = []
        for i in range(0, self.size):
            for j in range(0, self.size):
                self.free_positions.append((i,j))
        self.caging()

    def get_free_position_beta(self):
        return random.choice(self.free_positions)

    #TODO: Implement cages
    def caging(self):
        total_sum =  self.size * (self.size * (self.size + 1) / 2)
        while total_sum > 0:
            #pick a starting positions
            active = True
            free_values =  [ a for a in self.characters]
            pos = random.choice(self.free_positions) if len(self.free_positions) > 1 else self.free_positions[0]
            new_cage_positions = [(pos[0], pos[1], self.grid[pos[0]][pos[1]])]
            self.free_positions.remove(pos)
            free_values.remove(self.grid[pos[0]][pos[1]])

            while active == True:
                #check if there are any unused values(characters)left,  if not terminate caging
                if len(free_values) == 0:
                    active = False
                    break
                #neighbours of a cell, that aren't part of other cages and whose values don't appear in the current cage    
                valid_positions = [ r for r in self.get_available_neighbours(pos[0], pos[1]) if self.grid[r[0]][r[1]] in free_values]
                #if no valid positions are left, terminate
                if len(valid_positions) == 0:
                    active = False
                    break
                
                pos = random.choice(valid_positions) if len(valid_positions) > 1 else valid_positions[0]
                #update the cage positions, the free positions and the free values lists
                new_cage_positions.append((pos[0], pos[1], self.grid[pos[0]][pos[1]]))
                self.free_positions.remove(pos)
                free_values.remove(self.grid[pos[0]][pos[1]])
                #randomly interrupt the caging process, to create variety
                if len(new_cage_positions) > 1:
                    active = random.choice([True, False])
            #create a new cage with the new cage positions
            new_cage = Cage(new_cage_positions)
            self.cages.append(new_cage)
            total_sum-= new_cage.sum
                
            


    #subroutine for getting the neighbours of a cell, that aren't part of other cages, only vertical or horizontal neighbours
    def get_available_neighbours(self, x:int, y:int):
        neighbours = [(x-1, y), (x+1, y), (x, y-1),(x, y+1)]
        valid_neighbours = []
        for n in neighbours:
            if n[0] == -1 or n[1] == -1 or n[0] == self.size or n[1] == self.size or n not in self.free_positions:
                continue
            valid_neighbours.append(n)
            
        return valid_neighbours
    
    def __str__(self):
        st =  super().__str__()
        for cage in self.cages:
            st+=f"{cage}\n"
        return st


#TEST
k_s = KillerSudoku(monster=False)
print(k_s) 
import numpy as np

# set values for the grid
red = 1
yellow = -1
null = 0

move_map = {
    "X": 1,
    "O": -1,
}

class colours:
    RESET = "\033[0m"
    RED = "\033[31m"
    YELLOW = "\033[33m"

def display_val(val):
    if val == 1:
        return "X"
    if val == -1:
        return "O"
    return ""

def colour_val(val):
    if val == 1:
        return colours.RED
    if val == -1:
        return colours.YELLOW
    return " "

class Grid:
    def __init__(self, xdim=9, ydim=6, n=4, debug=False):
        self.debug = debug
        self.xdim = xdim
        self.ydim = ydim
        self.n = n # number in row required to win
        self.grid = np.array([[null for _ in range(self.ydim)] \
                                    for _ in range(self.xdim)])
        self.grid_counts = np.array([0 for _ in range(self.xdim)])
        self.init_grid_helpers()
        self.has_winner = False

    def init_grid_helpers(self):
        # grid helpers count extent in each direction
        self.grid_helpers = np.array([[[None for _ in range(4)] \
                                             for _ in range(self.ydim)] \
                                             for _ in range(self.xdim)])
        for i in range(self.xdim):
            for j in range(self.ydim):
                self.grid_helpers[i][j][0] = min(i, self.n-1) # west
                self.grid_helpers[i][j][2] = min(self.xdim-i-1, self.n-1) # east
                self.grid_helpers[i][j][1] = min(self.ydim-j-1, self.n-1) # north
                self.grid_helpers[i][j][3] = min(j, self.n-1) # south


    def reset_grid(self):
        self.grid *= 0
        self.grid_counts *= 0

    def get_valid_moves(self):
        # abs returns 1 if space is not empty
        return [i for i in range(self.xdim) if \
                np.sum(np.abs(self.grid[i][:])) != self.ydim]

    def is_valid_move(self, x):
        return x in self.get_valid_moves()
    
    def register_move(self, token, x):
        if self.is_valid_move(x):
            self.grid_counts[x] += 1
            self.grid[x][self.grid_counts[x]-1] = move_map[token]
            self.has_winner = self.check_for_winner(x,self.grid_counts[x]-1)
        else:
            print("invalid move.")

    def is_win(self,lst,len):
        # determines if a list is all the same and not 0s
        if lst[len-1] == 0: # check first element
            return False
        if lst[0] == 0: # check last element
            return False
        for i in range(1,len):
            if lst[i] != lst[0]:
                return False
        return True
    
    def check_for_winner(self,x,y):
        # vertical wins
        start = y-self.grid_helpers[x][y][3]
        end = y+self.grid_helpers[x][y][1]
        ny = (end - start + 2) - self.n
        for i in range(ny):
            if self.is_win(self.grid[x,start+i:start+i+self.n],self.n):
                return True

        # horizontal wins
        start = x-self.grid_helpers[x][y][0]
        end = x+self.grid_helpers[x][y][2]
        nx = (end - start + 2) - self.n
        for i in range(nx):
            if self.is_win(self.grid[start+i:start+i+self.n,y],self.n):
                return True

        # sw-ne diagonal wins
        list = self.grid.diagonal(0) # get diagonal
        offset = y-x
        list = self.grid.diagonal(offset) # get diagonal
        if offset < 0:
            pos = y
        else:
            pos = x
        start = pos - min(self.grid_helpers[x][y][0],self.grid_helpers[x][y][3])
        end = pos + min(self.grid_helpers[x][y][1],self.grid_helpers[x][y][2])
        nd = (end - start + 2) - self.n
        for i in range(nd):
            if self.is_win(list[start+i:start+i+self.n],self.n):
                return True

        # se-nw diagonal wins
        offset = y-(self.xdim-x-1)
        list = np.flipud(self.grid).diagonal(offset) # get diagonal
        if offset < 0:
            pos = y
        else:
            pos = self.xdim - x - 1
        start = pos - min(self.grid_helpers[x][y][2],self.grid_helpers[x][y][3])
        end = pos + min(self.grid_helpers[x][y][1],self.grid_helpers[x][y][0])
        nd = (end - start + 2) - self.n
        for i in range(nd):
            if self.is_win(list[start+i:start+i+self.n],self.n):
                return True    

        return False        

    def display(self):
        header = ""
        for i in range(self.xdim):
            header += "{} ".format(i+1)            
        print(header)
        header = ""
        for i in range(self.xdim - 1):
            header += "=="            
        header += "="
        print(header)

        for j in range(self.ydim -1, -1, -1):
            row_display = ""
            for i in range(self.xdim):
                row_display += "{}".format(display_val(self.grid[i][j]))
                print(colour_val(self.grid[i][j]) + \
                      "{}".format(display_val(self.grid[i][j])) + 
                      colours.RESET, end="")
                if i < self.xdim - 1:
                    row_display += "|"
                    print("|",end="")
            print()

        footer = ""
        for i in range(self.xdim - 1):
            footer += "=="            
        footer += "="
        print(footer)

    def get_state(self):
        # returns an 1 x (xdim x ydim) vector
        return tuple(self.grid.reshape(-1))
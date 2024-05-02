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
        else:
            print("invalid move.")

    def is_win(self,lst,len):
        # determines if a list is all the same and not 0s
        if lst[0] == 0:
            return False
        for i in range(1,len):
            if lst[i] != lst[0]:
                return False
        return True

    def has_winner(self):
        # vertical wins
        nx = self.xdim - self.n + 1 # row "freedom"
        ny = self.ydim - self.n + 1 # column "freedom"
        for j in range(ny):
            for i in range(self.xdim):
                if self.is_win(self.grid[i,j:j+self.n],self.n):
                    return True
        # horizontal wins
        for j in range(self.ydim):
            for i in range(nx):
                if self.is_win(self.grid[i:i+self.n,j],self.n):
                    return True
        # diagonal wins
        for i in range(1-nx,ny):
            # south-west to north-east wins
            list = self.grid.diagonal(i) # get diagonal
            nd = len(list) - self.n # diagonal "freedom"
            for j in range(nd+1):
                if self.is_win(list[j:j+self.n],self.n):
                    return True
            # south-east to north-west wins
            list = np.flipud(self.grid).diagonal(i) # get diagonal
            nd = len(list) - self.n # diagonal "freedom"
            for j in range(nd+1):
                if self.is_win(list[j:j+self.n],self.n):
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
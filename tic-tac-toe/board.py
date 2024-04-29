import numpy as np

x_vec = np.array([1, 0, 0])
o_vec = np.array([0, 1, 0])
null_vec = np.array([0, 0, 1])

def display_vector(vector):
    if (vector==x_vec).all():
        return "X"
    if (vector==o_vec).all():
        return "O"
    if (vector==null_vec).all():
        return " "

move_map = {
    "X": x_vec,
    "O": o_vec,
}

class Board:
    def __init__(self, debug=False):
        self.debug = debug
        self.reset_board()

    def reset_board(self):
        self.board = np.array([[null_vec for _ in range(3)] for _ in range(3)])

    def get_valid_moves(self):
        return [[i, j] for i in range(3) for j in range(3) if np.array_equal(self.board[i][j], null_vec)]

    def is_valid_move(self, x, y):
        return [x, y] in self.get_valid_moves()

    def register_move(self, player, x, y):
        self.board[x][y] = move_map[player]

    def has_winner(self):
        # Check rows and cols for (non-zero) winner
        for i in range(3):
            if not (self.board[i][0] == null_vec).all() and (self.board[i][0] == self.board[i][1]).all() and (self.board[i][0] == self.board[i][2]).all():
                return True
            if not (self.board[0][i] == null_vec).all() and (self.board[0][i] == self.board[1][i]).all() and (self.board[0][i] == self.board[2][i]).all():
                return True

        # Check diagonals for (non-zero) winner
        if not (self.board[0][0] == null_vec).all() and (self.board[0][0] == self.board[1][1]).all() and (self.board[0][0] == self.board[2][2]).all():
            return True
        if not (self.board[0][2] == null_vec).all() and (self.board[0][2] == self.board[1][1]).all() and (self.board[0][2] == self.board[2][0]).all():
            return True

        return False

    '''
    construct a human-readable board to print in console
    '''
    def display(self):
        for row in range(3):
            row_display = ""
            for col in range(3):
                # row_display += " {} ".format(display_vector(self.board[row][col]))
                row_display += " {} ".format(display_vector(self.board[col][2-row]))

                if col < 2:
                    row_display += "|"
            print(row_display)
        
            if row < 2:
                print("-----------")

import numpy as np

token_map = {
    "X": 1,
    "O": -1,
    " ": 0
}
inv_token_map = {v: k for k, v in token_map.items()}

class Board:
    def __init__(self, debug=False):
        self.debug = debug
        self.reset_board()

    def reset_board(self):
        self.board = np.zeros((3,3))

    def get_valid_moves(self):
        return [[i, j] for i in range(3) for j in range(3) if self.board[i][j] == 0]

    def is_valid_move(self, x, y):
        return [x, y] in self.get_valid_moves()

    def register_move(self, token, x, y):
        self.board[x][y] = token_map[token]

    def has_winner(self):
        # check rows
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != 0:
                return row[0]

        # check cols
        for col in range(len(self.board[0])):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != 0:
                return self.board[0][col]

        # check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != 0:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != 0:
            return self.board[0][2]

    def display(self):
        # construct a human-readable board to print in console
        for row in range(3):
            row_display = "{}  ".format([2-row])
            for col in range(3):
                row_display += " {} ".format(inv_token_map[self.board[col][2-row]])

                if col < 2:
                    row_display += "|"
            print(row_display)
        
            if row < 2:
                print("     -----------")
            
        print()
        print("     [0] [1] [2]")

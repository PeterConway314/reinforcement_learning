import random
import os

tokens = ["O", "X"]

def clear_screen():
    # Clear command for Windows
    if os.name == 'nt':
        os.system('cls')
    # Clear command for Unix-like systems (Linux, macOS)
    else:
        os.system('clear')

class Game:
    def __init__(self,grid,agent1,agent2):
        self.grid = grid
        self.agent1 = agent1
        self.agent2 = agent2
        self.turn_order = random.sample([agent1, agent2],2)

    def play_game(self):
        clear_screen()
        self.grid.display()
        while True:
            for i, agent in enumerate(self.turn_order):
                print("{}'s turn to move... ({} in a row needed to win)".format(tokens[i],self.grid.n))
                move = agent.select_move(self.grid.get_valid_moves())
                self.grid.register_move(tokens[i], move)
                clear_screen()
                self.grid.display()
                if self.grid.has_winner():
                    return print("{} wins!".format(tokens[i]))
                if not self.grid.get_valid_moves():
                    return print("draw.")
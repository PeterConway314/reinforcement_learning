import random
import os

tokens = ["O", "X"]

class Game:
    def __init__(self, board, agent1, agent2):
        self.board = board
        self.agent1 = agent1
        self.agent2 = agent2
        self.turn_order = random.sample([agent1, agent2], 2)

    def swap_turn(self):
        if self.active_agent == self.agent1:
            return self.agent2
        return self.agent1

    def play_game(self):
        while True:
            for i, agent in enumerate(self.turn_order):
                move = agent.select_move(self.board.get_valid_moves())
                self.board.register_move(tokens[i], move[0], move[1])
                os.system('cls')
                self.board.display()
                if self.board.has_winner():
                    return "{} wins!".format(tokens[i])

import random
import sys
sys.path.append("../utils/")
from utils import clear_screen

tokens = ["X", "O"]

class Game:
    def __init__(self, board, agent1, agent2):
        self.board = board
        self.agent1 = agent1
        self.agent2 = agent2
        self.randomise_move_order()

    def randomise_move_order(self):
        self.turn_order = random.sample([self.agent1, self.agent2], 2)
        self.agent_token_map = {
            self.turn_order[0]: tokens[0],
            self.turn_order[1]: tokens[1]
        }

    def game_step(self, agent):
        move = agent.select_move(self.board.get_valid_moves())
        self.board.register_move(self.agent_token_map[agent], move[0], move[1])

    def play(self):
        while True:
            for i, agent in enumerate(self.turn_order):
                self.game_step(agent)
                clear_screen()
                self.board.display()

                if self.board.has_winner():
                    return "{} wins!".format(tokens[i])
                if not self.board.get_valid_moves():
                    return "draw."

    def train(self, episodes):
        wins = 0
        draws = 0
        losses = 0

        for episode in range(episodes):
            print("{}/{}".format(episode, episodes))
            pass

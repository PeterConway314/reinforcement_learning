import random

class RandomAgent:
    def select_move(self, available_moves):
        return random.choice(available_moves)

class HumanAgent:
    def select_move(self, available_moves):
        while True:
            move = [int(x) for x in input("Please enter a valid move: ").split(',')]
            if move in available_moves:
                return move

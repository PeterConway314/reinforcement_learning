import random

class RandomAgent:
    def select_move(self, available_moves):
        return random.choice(available_moves)

class HumanAgent:
    def select_move(self, available_moves):
        while True:
            try:
                move = int(input("Please enter a valid move: ")) - 1
                if move in available_moves:
                    return move
            except ValueError:
                print("Invalid integer.")

from board import Board
from agents import HumanAgent, RandomAgent
from game import Game

if __name__ == "__main__":
    b = Board()
    me = HumanAgent()
    bot = RandomAgent()
    game = Game(b, me, bot)

    print(game.play_game())

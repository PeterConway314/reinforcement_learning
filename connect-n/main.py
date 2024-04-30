from grid import Grid
from agents import HumanAgent, RandomAgent
from game import Game

if __name__ == "__main__":
    g = Grid(10,10,6)
    p1 = HumanAgent()
    # p2 = HumanAgent()
    p2 = RandomAgent()
    game = Game(g,p1,p2)

    game.play_game()
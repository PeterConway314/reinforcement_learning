from board import Board
from agents import HumanAgent, RandomAgent, QLearningAgent
from game import Game

state_space_size = 9
action_space_size = 9

if __name__ == "__main__":
    b = Board()
    me = HumanAgent()
    # ai = QLearningAgent(state_space_size, action_space_size)
    rand = RandomAgent()
    game = Game(b, me, rand)
    print(game.play())

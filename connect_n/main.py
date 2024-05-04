from grid import Grid
from agents import HumanAgent, RandomAgent, BasicQAgent
from game import Game

XDIM = 5
YDIM = 5
N = 4

if __name__ == "__main__":
    g = Grid(XDIM,YDIM,N)
    p1 = HumanAgent()
    # p2 = HumanAgent()
    p2 = RandomAgent()
    # p1 = BasicQAgent(XDIM*YDIM,N)
    # p1 = p1.load_agent_by_name("jenson")
    # p1.epsilon = 0 # disable exploration
    game = Game(g,p1,p2)

    game.play()
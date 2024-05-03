from grid import Grid
from agents import HumanAgent, BasicQAgent, RandomAgent
from game import TrainingGame, Game
import matplotlib.pyplot as plt
import random

XDIM = 4 # board width
YDIM = 4 # board height
N = 3 # number in a row to win
NUM_EPS = 100 # total episodes
PER_EP = 100 # num games per episode

random.seed(0)

class Trackers():
    def __init__(self):
        self.x = []
        # raw data
        self.wins = []
        self.losses = []
        self.draws = []
        # mean data
        self.wins_mean = []

trackers = Trackers()

def update_plots(show_result=False):
    plt.figure(1)
    if show_result:
        plt.title('Result')
    else:
        plt.clf()
        plt.title('Training...')
    plt.xlabel('Episode')
    plt.ylabel('%')
    plt.plot(trackers.wins, label='win rate')
    plt.plot(trackers.losses, label='loss rate')
    plt.plot(trackers.draws, label='draw rate')

    if len(trackers.x) >= 100:
        trackers.wins_mean.append(sum(trackers.wins[-100:])/100)
        plt.plot(trackers.x[99:],trackers.wins_mean, label='win rate (mean)')

        last_mean = trackers.wins_mean[-1]
        plt.plot([0, len(trackers.x) - 1], [last_mean, last_mean], color='k', linestyle='--')
        plt.text(len(trackers.x) - 1, last_mean + 3, f'{last_mean:.2f} %', ha='right', va='center', color='k')



    plt.ylim(0,100)
    plt.legend()
    plt.pause(0.001)

def __main__():
    g = Grid(XDIM,YDIM,N)
    # p1 = HumanAgent()
    # p2 = HumanAgent()
    # p1 = RandomAgent()
    p1 = BasicQAgent(XDIM*YDIM,N)
    # p1 = p1.load_agent_by_name("jenson")
    
    p2 = RandomAgent()
    # p2 = BasicQAgent(XDIM*YDIM,N)
    # p2 = p2.load_agent_by_name("jenson")
    # p2.load_agent_by_episode(1000)
    # p2.epsilon = 0
    # p2.can_learn = False
    # game = Game(g,p1,p2)
    
    game = TrainingGame(g,p1,p2)

    wins = 0
    losses = 0
    draws = 0

    for i in range(NUM_EPS):
        wins = 0
        losses = 0
        draws = 0
        for _ in range(PER_EP):
            game.grid.reset_grid()
            outcome = game.train()
            if outcome == 0:
                wins += 1
            elif outcome == 1:
                losses += 1
            else:
                draws += 1

        trackers.wins.append(wins/PER_EP*100)
        trackers.losses.append(losses/PER_EP*100)
        trackers.draws.append(draws/PER_EP*100)
        trackers.x.append(i)
        update_plots()

    print(f"complete")
    p1.save_agent(NUM_EPS*PER_EP)
    plt.show()


if __name__ == "__main__":
    __main__()    
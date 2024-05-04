import random
import os
import numpy as np

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

    def play(self):
        turn_order = random.sample([self.agent1,self.agent2], 2)
        clear_screen()
        self.grid.display()
        while True:
            for i, agent in enumerate(turn_order):
                print("{}'s turn to move... ({} in a row needed to win)".format(tokens[i],self.grid.n))
                state = self.grid.get_state() # get state
                move = agent.select_move(state,self.grid.get_valid_moves())
                self.grid.register_move(tokens[i], move)
                clear_screen()
                self.grid.display()
                if self.grid.has_winner:
                    return print("{} wins!".format(tokens[i]))
                if not self.grid.get_valid_moves():
                    return print("draw.")

class TrainingGame(Game):
    # Game subclass, which updates q values and states etc...
    def __init__(self, *args):
        super().__init__(*args)
        self.prev_states = [None] * 2 # init first state
        self.recent_actions = [None] * 2 # init most recent action
        self.state = self.grid.get_state() # init game state

    def randomise_start(self):
        self.agents = random.sample([self.agent1,self.agent2],2) # random turn order
        self.agent_tokens = random.sample(tokens,2) # random tokens

    def update_q_value(self,i,reward=0):
        self.agents[i].update_q_value( # update q-val
                self.prev_states[i],
                self.recent_actions[i],
                reward,
                self.state
            )

    def move_cycle(self,i,first_cycle=False):
        agent = self.agents[i] # get agent
        token = self.agent_tokens[i] # get agent token
        if not first_cycle:
            self.update_q_value(i) # neutral q-value update
        self.prev_states[i] = self.state # save state when action was made
        action = agent.select_move(self.state, self.grid.get_valid_moves())
        self.recent_actions[i] = action # save action made
        self.grid.register_move(token, action) # do action
        self.state = self.grid.get_state() # get updated state

    def train(self):
        self.randomise_start() # randomise the turn order and tokens
        # first cycle
        for i in [0,1]:
            self.move_cycle(i,first_cycle=True) # make move with no q-val update

        # main loop
        while True: # while not finished
            for i in [0, 1]: # cycle through agents
                self.move_cycle(i) # make move
                if self.grid.has_winner: # if winner
                    self.update_q_value(i,reward=1) # reward winner
                    self.update_q_value(np.mod(i+1,2),reward=-1) # penalise loser
                    if self.agents[i] == self.agent1: # get return value
                        return 0
                    else:
                        return 1
                else: # if no winner
                    if not self.grid.get_valid_moves(): # if no available moves
                        self.update_q_value(i,reward=0.1) # small reward
                        self.update_q_value(np.mod(i+1,2),reward=0.1) # small reward
                        return 2
import random
import os
import pickle

dirname = os.path.dirname(__file__)

class RandomAgent:
    def select_move(self, state, available_moves):
        return random.choice(available_moves)

    def update_q_value(*args):
        pass
    
class HumanAgent:
    def select_move(self, state, available_moves):
        while True:
            try:
                move = int(input("Please enter a valid move: ")) - 1
                if move in available_moves:
                    return move
            except ValueError:
                print("Invalid integer.")

    def update_q_value(*args):
        pass

class BasicQAgent:
    def __init__(self, state_space_size, action_space_size, learning_rate=0.1, discount_factor=0.9, epsilon=0.1, can_learn=True):
        self.state_space_size = state_space_size  # Number of possible states
        self.action_space_size = action_space_size  # Number of possible actions
        self.learning_rate = learning_rate  # Learning rate (alpha)
        self.discount_factor = discount_factor  # Discount factor (gamma)
        self.epsilon = epsilon  # Epsilon for epsilon-greedy policy
        self.Q_table = {}  # Q-table to store Q-values
        self.can_learn = can_learn # whether or not agent can learn

    def save_agent(self,episode_num):
        print(f"saving agent...")
        with open(os.path.join(dirname, '.', 'models', f'basic_agent_{episode_num}.pickle'), 'wb') as handle:
            pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL) 
        print(f"agent saved.")

    def load_agent_by_episode(self, episode_num):
        print(f"loading agent...")
        with open(os.path.join(dirname, '.', 'models', f'basic_agent_{episode_num}.pickle'), 'rb') as handle:
            agent = pickle.load(handle)
        print(f"agent loaded.")
        return agent

    def load_agent_by_name(self, name):
        print(f"loading agent...")
        with open(os.path.join(dirname, 'models', f'{name}.pickle'), 'rb') as handle:
            agent = pickle.load(handle)
        print(f"agent loaded.")
        return agent

    def select_move(self, state, available_actions):
        """
        Epsilon-greedy action selection based on Q-values.
        """
        
        if random.uniform(0, 1) < self.epsilon:
            # Exploration: Choose a random action from the available actions
            return random.choice(available_actions)
        else:
            # Exploitation: Choose the action with the highest Q-value for the current state
            if state in self.Q_table:
                # print(f"state exists")
                q_values = {}
                for action, value in self.Q_table[state].items():
                    if action in available_actions:
                        q_values[action] = value
                
                if q_values: # if q-values exist at this state
                    # print(f"q vals: {q_values}")
                    # x = input()
                    return max(q_values, key=q_values.get)
                else: # else, random choice
                    return random.choice(available_actions)
            else:
                # If state not in Q-table, choose a random action from the available actions
                return random.choice(available_actions)

    def update_q_value(self, state, action, reward, next_state):
        """
        Update Q-value based on the Q-learning update rule.
        """
        if self.can_learn:
            # Ensure states are in Q_table
            if state not in self.Q_table:
                self.Q_table[state] = {}
            if next_state not in self.Q_table:
                self.Q_table[next_state] = {}

            # Q-learning update rule
            if self.Q_table[next_state]: # if q-values exist at next state
                max_next_q_value = max(self.Q_table[next_state].values())
            else:
                max_next_q_value = 0
            td_target = reward + self.discount_factor * max_next_q_value
            try:
                td_error = td_target - self.Q_table[state][action]
            except KeyError:
                # If the key doesn't exist, assign a default value (e.g., 0)
                self.Q_table[state][action] = 0
                td_error = td_target  # Assume Q-value is 0
            self.Q_table[state][action] += self.learning_rate * td_error

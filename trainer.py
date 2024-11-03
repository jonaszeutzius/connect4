import numpy as np
from random import choice
from connect4 import Connect4Board

class Connect4Agent:
    def __init__(self):
        self.action_size = 7  # Number of columns
        self.states = []  # To store the states and actions
        self.rewards = []  # To store rewards for each step

    def choose_action(self, board, epsilon):
        if np.random.rand() < epsilon:
            # Explore: choose a random valid action
            valid_moves = [col for col in range(board.columns) if board.board[board.rows - 1, col] == 0]
            return choice(valid_moves)
        else:
            # Exploit: choose the best action (random for now)
            return choice([col for col in range(board.columns) if board.board[board.rows - 1, col] == 0])

    def store_data(self, state, action, reward):
        self.states.append(state)
        self.rewards.append(reward)

def play_game(agent1, agent2, epsilon):
    board = Connect4Board()
    current_agent = agent1
    while True:
        state = board.board.copy()  # Record the current state
        action = current_agent.choose_action(board, epsilon)
        
        try:
            board.drop_piece(action)
        except ValueError as e:
            print(f"Error: {e}")  # Handle invalid moves (optional)
            continue

        # Check for win
        if board.check_for_win(1)[0]:  # Player 1
            current_agent.store_data(state, action, 1)  # Reward for winning
            break
        elif board.check_for_win(-1)[0]:  # Player 2
            current_agent.store_data(state, action, -1)  # Reward for losing
            break
        elif np.all(board.board != 0):  # Check for draw
            current_agent.store_data(state, action, 0)  # No reward for draw
            break

        # Switch agents
        current_agent = agent2 if current_agent == agent1 else agent1

# Initialize agents
agent1 = Connect4Agent()
agent2 = Connect4Agent()

# Collect data through self-play
for episode in range(1000):  # Play 1000 games
    play_game(agent1, agent2, epsilon=0.1)  # Adjust epsilon as needed

# Now agent1.states and agent1.rewards contain the collected training data

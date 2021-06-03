from tictactoe import TicTacToe, hash_state, invert_hash, is_game_over, make_move
import random

value_fn = {}

class Agent:
    def __init__(self, player_id):
        self.player_id = player_id
        self.last_action = None
        self.last_state = None
        self.alpha = 0.1
        self.epsilon = 0.1
    
    def act(self, state, available_actions):
        if random.random() < self.epsilon:
            return random.choice(available_actions)
        else:
            return self.greedy_action(state, available_actions)
    
    def greedy_action(self, state, available_actions):
        available_values = []
        state_unhashed = invert_hash(state)
        for action in available_actions:
            next_state = make_move(state_unhashed, self.player_id, action)
            next_val = self.get_value(hash_state(next_state))
            available_values.append(next_val)

        if self.player_id == 0:
            indices = self.best_indices(available_values, max)
        else:
            indices = self.best_indices(available_values, min)

        # tie breaking by random choice
        idx = random.choice(indices)
        action = available_actions[idx]

        return action

    def best_indices(self, values, fn):
        best = fn(values)
        return [i for i, v in enumerate(values) if v == best]

    def get_value(self, state):
        if state not in value_fn:
            winner = is_game_over(invert_hash(state))
            if winner is None:
                value_fn[state] = 0
            else:
                value_fn[state] = 1 if self.player_id == 0 else -1
        return value_fn[state]

    def backup(self, state, next_state, reward):
        val = self.get_value(state)
        next_val = self.get_value(next_state)
        val = val + self.alpha * (next_val - val)
        value_fn[state] = val

if __name__ == '__main__':
    ttt = TicTacToe()

    # ttt.render()
    agent1 = Agent(0)
    agent2 = Agent(1)
    num_episodes = 5000
    scores_0 = 0
    scores_1 = 0
    for i in range(num_episodes):
        ttt.reset()
        done = False
        state, next_player = hash_state(ttt.state), ttt.next_player
        while not done:
            available_actions = [i for i, v in enumerate(ttt.is_action_possible) if v]
            if next_player == 0:
                agent = agent1
            else:
                agent = agent2
            action = agent.act(state, available_actions)
            next_state, next_player, reward, done = ttt.step(action)
            agent.backup(state, next_state, reward)
            if reward == 1:
                scores_0 += 1
            elif reward == -1:
                scores_1 += 1
        print(scores_0, " ", scores_1)
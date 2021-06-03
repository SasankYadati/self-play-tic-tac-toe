from tictactoe import MARKERS, TicTacToe, hash_state, invert_hash, is_game_over, make_move, print_board
import random

class Agent:
    def __init__(self, player_id):
        self.player_id = player_id
        self.value_fn = {}
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

        indices = self.best_indices(available_values, max)
        idx = random.choice(indices)
        action = available_actions[idx]

        return action

    def best_indices(self, values, fn):
        best = fn(values)
        return [i for i, v in enumerate(values) if v == best]

    def get_value(self, state):
        if state not in self.value_fn:
            winner = is_game_over(invert_hash(state))
            if winner is None:
                self.value_fn[state] = 0
            else:
                self.value_fn[state] = 1 if self.player_id == MARKERS.index(winner) else -1
        return self.value_fn[state]

    def backup(self, state, next_state):
        val = self.get_value(state)
        next_val = self.get_value(next_state)
        val = val + self.alpha * (next_val - val)
        self.value_fn[state] = val

if __name__ == '__main__':
    ttt = TicTacToe(start_player=1)

    # ttt.render()
    agents = [Agent(0),Agent(1)]
    scores = [0, 0]

    num_episodes = 5000
    i = 0
    while i<num_episodes:
        ttt.reset()
        done = False
        state, next_player = hash_state(ttt.state), ttt.next_player
        while not done:
            available_actions = [i for i, v in enumerate(ttt.is_action_possible) if v]
            agent = agents[next_player]
            action = agent.act(state, available_actions)
            next_state, next_player, reward, done = ttt.step(action)
            # ttt.render()
            agents[0].backup(state, next_state)
            agents[1].backup(state, next_state)
        if reward == 1:
            scores[1-next_player] += 1
        if (i%1000 == 0):
            print(scores)
            scores = [0,0]
        i+=1
    for state in agents[0].value_fn.keys():
        if (agents[0].value_fn[state] not in [0, 1, -1]):
            print_board(invert_hash(state))
            print(agents[0].value_fn[state])
            print(agents[1].value_fn[state])
            print("\n\n\n")

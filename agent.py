from tictactoe import MARKERS, TicTacToe, hash_state, invert_hash, is_game_over, is_tied, make_move, print_board
import random

class Agent:
    def __init__(self, player_id):
        self.player_id = player_id
        self.value_fn = {}
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
                self.value_fn[state] = 0.5 if is_tied(invert_hash(state)) else 0.0 
            else:
                self.value_fn[state] = 1.0 if self.player_id == MARKERS.index(winner) else -1.0
        return self.value_fn[state]

    def backup(self, state, next_state):
        val = self.get_value(state)
        next_val = self.get_value(next_state)
        val = val + self.alpha * (next_val - val)
        self.value_fn[state] = val
    
    def print_values(self, nsamples=3):
        for state in self.value_fn.keys():
            if (self.value_fn[state] not in [0,1,-1]):
                print_board(invert_hash(state))
                print(self.value_fn[state])
                print("\n\n\n")
            nsamples-=1
            if nsamples == 0:
                return

if __name__ == '__main__':

    agents = [Agent(0),Agent(1)]
    scores = [0, 0]

    num_episodes = 50000
    i = 1
    while i<num_episodes:
        ttt = TicTacToe(start_player=i%2)
        ttt.reset()
        done = False
        state, next_player = hash_state(ttt.state), ttt.next_player
        while not done:
            available_actions = [i for i, v in enumerate(ttt.is_action_possible) if v]
            action = agents[next_player].act(state, available_actions)
            next_state, next_player, reward, done = ttt.step(action)
            agents[0].backup(state, next_state)
            agents[1].backup(state, next_state)
            state = next_state
        if reward == 1:
            winner = is_game_over(invert_hash(state))
            scores[MARKERS.index(winner)] += 1
        if i%1000 == 0:
            print(scores)
            scores = [0,0]
        i+=1
    # print(agents[0].print_values())
    # print(agents[1].print_values())
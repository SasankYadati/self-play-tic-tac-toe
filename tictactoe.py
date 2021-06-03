from gym import spaces
MARKERS = ['X', 'O']

class TicTacToe:
    def __init__(self, start_player=0):
        self.action_space = spaces.Discrete(9)
        self.initial_state = ['-']*9
        self.start_player = start_player
        self.reset()

    def reset(self):
        self.state = self.initial_state
        self.is_action_possible = [True]*9
        self.num_possible_actions = 9
        self.state = self.initial_state
        self.next_player = self.start_player

    def step(self, action):
        assert self.is_action_possible[action], f"Action is invalid"
        curr_player = self.next_player
        self.state = make_move(self.state, curr_player, action)
        self.is_action_possible[action] = False
        self.num_possible_actions -= 1
        winner = is_game_over(self.state)
        done = self.num_possible_actions == 0 or winner is not None
        reward = 0
        if done and winner is not None:
            reward = 1
        self.next_player = 1 - curr_player
        return hash_state(self.state), self.next_player, reward, done

    def render(self):
        print_board(self.state)

    def sample_action(self):
        random_action = self.action_space.sample()
        while self.is_action_possible[random_action] is False:
            random_action = self.action_space.sample()
        return random_action

def print_board(state):
    print ( "   |   |   ")
    print (f" {state[0]} | {state[1]} | {state[2]}  ")
    print ("   |   |")
    print ("---|---|---")
    print ("   |   |")
    print (f" {state[3]} | {state[4]} | {state[5]}  ")
    print ("   |   |")
    print ("---|---|---")
    print ("   |   |")
    print (f" {state[6]} | {state[7]} | {state[8]}  ")
    print ("   |   |   ")
    print("------------")
    print("------------")
    
def hash_state(state):
    hash = ",".join([s for s in state])
    return hash

def invert_hash(hash):
    return hash.split(",")

def is_game_over(state):
    winner = checkDiagonal(state)
    if (winner is None):
        winner = checkRows(state)
        if (winner is None):
            return checkColumns(state)
        else:
            return winner
    else:
        return winner

def checkDiagonal(state):
    if (state[0] == state[4] == state[8] and state[0] in MARKERS):
        return state[0]
    elif (state[2] == state[4] == state[6] and state[2] in MARKERS):
        return state[2]
    return None

def checkRows(state):
    if (state[0] == state[1] == state[2] and state[0] in MARKERS):
        return state[0]
    elif (state[3] == state[4] == state[5] and state[3] in MARKERS):
        return state[3]
    elif (state[6] == state[7] == state[8] and state[6] in MARKERS):
        return state[6]
    return None

def checkColumns(state):
    if (state[0] == state[3] == state[6] and state[0] in MARKERS):
        return state[0] 
    elif (state[1] == state[4] == state[7] and state[1] in MARKERS):
        return state[1]
    elif (state[2] == state[5] == state[8] and state[2] in MARKERS):
        return state[2]
    return None

def make_move(state, player, action):
    assert state[action] == '-', "Action invalid"
    next_state = state[:]
    next_state[action] = MARKERS[player]
    return next_state
import numpy as np
from collections import defaultdict
from ultimate_tictactoe import UltimateTicTacToe

class MCTS_agent:
    def __init__(self, computational_budget, start_state, player:int = 1) -> None:
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        #Remember to construct the state map as we expand outward.
        # each visit to a state should check if the string is in self.states and if not add it
        # with the current expected score/0
        self.budget = computational_budget
        self.current_state = start_state

    def tree_policy(self):
        counter = 0
        while counter <= self.budget:
            child = np.random.choice(self.states[self.current_state].keys())
            while len(self.states[child])   
        pass

    def choose(self, node):
        "Choose the best successor of node. (Choose a move in the game)"
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average reward

        return max(self.children[node], key=score)

    def simulation(self, current_board:UltimateTicTacToe):
        board = current_board.copy()
        won = board.winner
        moves = {}
        while won not in (1,-1,0):
            move = self.get_move(board)

            moves[board.copy()] = won

            won = board.play(move)

        moves["results"] = (str(board), won)
        return moves

    def get_move(self, board:UltimateTicTacToe):
        moves = board.legal_moves()
        #Picks a move uniformly
        return np.random.choice(moves)

    def backpropagation(self, moves):
        pass

    def round(self, game_object):
        pass




import itertools
from os import pread
import numpy as np
from abc import ABC, abstractmethod
from collections import defaultdict
import math

BOARD_SIZE = 9 # Must be a square of a natural number
class UTTNode:
    """
    A representation of a single board state.
    MCTS works by constructing a tree of these Nodes.
    Could be e.g. a chess or checkers board state.

    If there are no more moves and no one has won, then draw
    player 1 is X
    """
    def __init__(self, previous_move=None, current_player = 1):
        self.top_board = np.zeros(BOARD_SIZE)
        self.bot_boards = {i: np.zeros(BOARD_SIZE) for i in range(BOARD_SIZE)}
        self.prev_move = previous_move
        self.current_player = current_player
    
    def play(self, move) -> int:
        
        # Do not mutate when move is illegal. User of method must verify this beforehand.
        if not self.is_legal(move):
            raise ValueError("Illegal move : move attempted outside legal selection")
        
        #Playing move
        self.bot_boards[move[0]][move[1]] = self.current_player

        self.current_player *= -1
        self.prev_move = move[0]

        if self.is_terminal():
            return self.reward()
        else:
            return None

    def legal_moves(self):
        top_board = self.bot_board[self.prev_move] if self.top_board[self.prev_move] == 0 else None
        moves = []
        if top_board is None:
            top = [index for index, value in enumerate(top_board) if value == 0]
        else:
            top = [top_board]
        for board_num in top:
            moves.append([(board_num, position) for position in self.bottom_board[board_num] if position == 0])
        return moves
    
    def copy(self):
        return UTTNode(previous_move=self.prev_move, current_player = self.current_player)

    def is_legal(self, action):
        return (max(action) <9
                and min(action) >=0)

    def find_children(self):
        "All possible successors of this board state"
        if self.is_terminal():
            return set()
        else:
            return set(self.copy().play(move) for move in self.legal_moves())

    def find_random_child(self):
        "Random successor of this board state (for more efficient simulation)"
        return np.random.choice(self.legal_moves())

    def is_terminal(self):
        board = np.array(self.top_board).reshape(3,3)
        return (np.all(board,axis=0).any() # 3 in a row horizontally/vertically
            or np.all(board,axis=1).any()
            or np.all(board.diagonal()) # 3 in a row on the diagonal
            or np.all(np.flipud(board).diagonal())
            or not 0 in self.top_board)

    def reward(self):
        board = np.array(self.top_board).reshape(3,3)
        if (np.all(board,axis=0).any() # 3 in a row horizontally/vertically
            or np.all(board,axis=1).any()
            or np.all(board.diagonal()) # 3 in a row on the diagonal
            or np.all(np.flipud(board).diagonal())):
            return self.current_player
        else:
            return 0.5

    def __eq__(node1, node2):
        return str(node1) == str(node2)
    
    def __str__(self):
        return ''.join(self.bot_boards.values())


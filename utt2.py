import numpy as np
from abc import ABC, abstractmethod
from collections import defaultdict
import math

BOARD_SIZE = 9 # Must be a square of a natural number
WIN_X = np.array([1,1,1])
WIN_O = np.array([-1,-1,-1])
class UTTNode:
    """
    A representation of a single board state.
    MCTS works by constructing a tree of these Nodes.
    Could be e.g. a chess or checkers board state.

    If there are no more moves and no one has won, then draw
    player 1 is X
    """
    def __init__(self, previous_move=None, current_player = 1):
        self.top_board = np.zeros(BOARD_SIZE, dtype=int)
        self.bot_boards = {i: np.zeros(BOARD_SIZE, dtype = int) for i in range(BOARD_SIZE)}
        self.prev_move = previous_move
        self.current_player = current_player
    
    def play(self, move) -> int:
        
        # Do not mutate when move is illegal. User of method must verify this beforehand.
        if not self.is_legal(move):
            raise ValueError("Illegal move : move attempted outside legal selection")
        
        #Playing move
        self.bot_boards[move[0]][move[1]] = self.current_player

        if self.subterminal(move[0]):
            #print("TERMINATED:", move[0])
            self.top_board[move[0]] = self.subwin(move[0])
            self.prev_move = None
        else:
            self.prev_move = move[1]


        self.current_player *= -1
        
        if self.is_terminal():
            return self.reward()    
        else:
            return None

    def legal_moves(self):
        """
        All legal moves are of the tuple form (i,j) where i is the index of a given TTT board,
            and j is the index within that board 
        """
        moves = []
        if self.prev_move is None:
            top = [index for index, value in enumerate(self.top_board) if value == 0]
        elif self.top_board[self.prev_move] == 0:
            top = [self.prev_move]
        else:
            top = [index for index, value in enumerate(self.top_board) if value == 0]
        #print(top)
        for board_num in top:
            moves+=[(board_num, index) for index, position in enumerate(self.bot_boards[board_num]) if position == 0]
        return moves
    
    def copy(self):
        new_node = UTTNode(previous_move=self.prev_move, current_player = self.current_player)
        new_node.top_board = self.top_board.copy()
        new_node.bot_boards = self.bot_boards.copy()
        return new_node

    def is_legal(self, action):
        return (max(action) <9
                and min(action) >=0)
    
    def subterminal(self, boardnum):
        board = np.array(self.bot_boards[boardnum]).reshape(3,3)
        return (np.all(board == WIN_X,axis=0).any() # 3 in a row horizontally/vertically
            or np.all(board == WIN_X,axis=1).any()
            or np.all(board.diagonal() == WIN_X) # 3 in a row on the diagonal
            or np.all(np.flipud(board).diagonal() == WIN_X)
            or np.all(board == WIN_O,axis=0).any() # 3 in a row horizontally/vertically
            or np.all(board == WIN_O,axis=1).any()
            or np.all(board.diagonal() == WIN_O) # 3 in a row on the diagonal
            or np.all(np.flipud(board).diagonal() == WIN_O)
            or not 0 in board)


    def subwin(self, boardnum):
        board = np.array(self.bot_boards[boardnum]).reshape(3,3)
        if (np.all(board == WIN_X,axis=0).any() # 3 in a row horizontally/vertically
            or np.all(board == WIN_X,axis=1).any()
            or np.all(board.diagonal() == WIN_X) # 3 in a row on the diagonal
            or np.all(np.flipud(board).diagonal() == WIN_X)
            or np.all(board == WIN_O,axis=0).any() # 3 in a row horizontally/vertically
            or np.all(board == WIN_O,axis=1).any()
            or np.all(board.diagonal() == WIN_O) # 3 in a row on the diagonal
            or np.all(np.flipud(board).diagonal() == WIN_O)):
            return self.current_player
        else:
            return 999


    def find_children(self):
        "All possible successors of this board state"
        if self.is_terminal():
            return set()
        else:
            return set(self.copy().play(move) for move in self.legal_moves())

    def find_random_child(self):
        "Random successor of this board state (for more efficient simulation)"
        return tuple(np.random.default_rng().choice(self.legal_moves, 1, replace=False, axis = 0)[0])

    def is_terminal(self):
        board = np.array(self.top_board).reshape(3,3)
        return (np.all(board == WIN_X,axis=0).any() # 3 in a row horizontally/vertically
            or np.all(board == WIN_X,axis=1).any()
            or np.all(board.diagonal() == WIN_X) # 3 in a row on the diagonal
            or np.all(np.flipud(board).diagonal() == WIN_X)
            or np.all(board == WIN_O,axis=0).any() # 3 in a row horizontally/vertically
            or np.all(board == WIN_O,axis=1).any()
            or np.all(board.diagonal() == WIN_O) # 3 in a row on the diagonal
            or np.all(np.flipud(board).diagonal() == WIN_O)
            or not 0 in board)

    def reward(self):
        board = np.array(self.top_board).reshape(3,3)
        if (np.all(board == WIN_X,axis=0).any() # 3 in a row horizontally/vertically
            or np.all(board == WIN_X,axis=1).any()
            or np.all(board.diagonal() == WIN_X) # 3 in a row on the diagonal
            or np.all(np.flipud(board).diagonal() == WIN_X)
            or np.all(board == WIN_O,axis=0).any() # 3 in a row horizontally/vertically
            or np.all(board == WIN_O,axis=1).any()
            or np.all(board.diagonal() == WIN_O) # 3 in a row on the diagonal
            or np.all(np.flipud(board).diagonal() == WIN_O)):
            return self.current_player
        else:
            return 0

    def __eq__(node1, node2):
        return str(node1) == str(node2)
    
    """def __str__(self):
        return ''.join([str(board_val) for board_val in self.bot_boards.values()])"""

    def __str__(self):
        marks = ["_", "x", "o"]
        result = ""
        for board in range(0,9,3):
            for row in range(0,9,3):
                result+=(" ".join([marks[int(board_val)] for board_val in self.bot_boards[board][row:row+3]])
                + "  " + " ".join([marks[int(board_val)] for board_val in self.bot_boards[board+1][row:row+3]])
                + "  " + " ".join([marks[int(board_val)] for board_val in self.bot_boards[board+2][row:row+3]]))
                if row+3 == 9:
                    result+="\n\n"
                else:
                    result+="\n"
        return result
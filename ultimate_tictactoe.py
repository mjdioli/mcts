import numpy as np
import itertools

UTTT_SHAPE = (3,3,3,3)
TTT_SHAPE = (3,3)

class UltimateTicTacToe:
    
    
    def __init__(self, board=np.zeros(UTTT_SHAPE), select=np.ones(TTT_SHAPE), wins=np.zeros(TTT_SHAPE), player=1, turn=0):
        self.board = np.copy(board)
        self.select = np.copy(select)
        self.wins = np.copy(wins)
        if player not in (-1, 1):
            raise ValueError(f"Player must be 1 (X) or -1 (O), player was {player}")
        self.player = player #x starts
        self.turn = turn
    
    
    def immutable_transition_function(self, action : tuple):
        game_copy = UltimateTicTacToe(self.board, self.select, self.wins, self.player, self.turn)
        winner = game_copy.mutable_transition_function(action)
        return game_copy, winner
    
    
    def mutable_transition_function(self, action : tuple) -> int:
        # Insist that the action must be of type tuple, as lists and tuples
        # behave differently when used as indices
        action = tuple(action)
        outer_select, inner_select = action[:2], action[2:]
        
        # Do not mutate when move is illegal. User of method must verify this beforehand.
        if ( max(action) > 2 # Move is within the board
                or min(action) < 0
                or (not self.select[outer_select]) # Outer selection (2 first axes) is permitted by previous move
                or self.board[action] ): # square is not taken
            raise ValueError("Illegal move : move attempted outside legal selection")
        
        # Set square to be taken by the current player ( -1 or 1, corresponding to either X or O)
        self.board[action] = self.player
        
        # Mark the inner board as won if won, or draw if draw
        if ( player := UltimateTicTacToe.winner( self.board[outer_select] ) ):
            self.wins[outer_select] = player
            # If the updated win table results in an overall win (or draw), return which player won (or 2 if draw).
            if (winner := UltimateTicTacToe.winner(self.wins)):
                return winner
        
        # If the next inner board to play as defined by the two last axes of the move,
        # is already won or drawn, the next player can choose which inner board they want to play.
        if self.wins[inner_select]:
            # A free selection of inner boards is all the boards which aren't already won or drawn.
            self.select = np.ones(TTT_SHAPE) - (self.wins != 0)
        else:
            # Otherwise, the next board to play is defined by the two last axes of the move
            self.select = np.zeros(TTT_SHAPE)
            self.select[inner_select] = 1
        if not self.select.any():
            return 2
        self.player *= -1
        self.turn += 1
        return 0 #No winner
    
    
    def play(self, move):
        return self.mutable_transition_function(move)
    
    
    def winner(board):
        return 1 if UltimateTicTacToe.is_win(board==1) else -1 if UltimateTicTacToe.is_win(board==-1) else 2 if UltimateTicTacToe._is_draw(board) else 0
    
    
    def is_win(board):
        return (np.all(board,axis=0).any() # 3 in a row horizontally/vertically
            or np.all(board,axis=1).any()
            or np.all(board.diagonal()) # 3 in a row on the diagonal
            or np.all(np.flipud(board).diagonal()))
    
    
    def _is_draw(board):
        # Assuming not win
        return (board != 0).all()
    
    def legal_moves(self):
        moves = np.zeros(UTTT_SHAPE)
        outer_indices = self.select.nonzero()
        # The legal moves are all the empty squares in the inner boards permitted by the previous move
        moves[outer_indices] = self.board[outer_indices] == 0
        return moves
    
    
    def __str__(self):
        result = ""
        for idc, n in zip(itertools.product(*[range(3)]*4), range(81)):
            if n > 0:
                result += "\n\n" if (n % 27 == 0)  else "\n" if (n % 9 == 0) else "  " if (n % 3 == 0) else " "
            idc = tuple(np.array(idc)[[0,2,1,3]])
            result += ["_", "X", "O"][int(self.board[idc])]
        return result

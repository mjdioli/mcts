import numpy as np

UTTT_SHAPE = (3,3,3,3)
TTT_SHAPE = (3,3)

class UltimateTicTacToe:
    
    
    def __init__(self, board=np.zeros(UTTT_SHAPE), select=np.ones(TTT_SHAPE), wins=np.zeros(TTT_SHAPE), player=1, turn=0):
        self.board = board
        self.select = select
        self.wins = wins
        if player not in (-1, 1):
            raise ValueError(f"Player must be 1 (X) or -1 (O), player was {player}")
        self.player = player #x starts
        self.turn = turn
    
    
    def immutable_transition_function(self, action : tuple):
        game_copy = UltimateTicTacToe(np.copy(self.board), np.copy(self.select), np.copy(self.wins), self.player, self.turn)
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
        
        # Mark the inner board as won if won
        if UltimateTicTacToe.winner(self.board[outer_select]):
            self.wins[outer_select] = self.player
            # If the updated win table results in an overall win, return which player won.
            if (winner := UltimateTicTacToe.winner(self.wins)):
                return winner
        
        # If the next inner board to play as defined by the two last axes of the move,
        # is already won, the next player can choose which inner board they want to play.
        if UltimateTicTacToe.winner(self.board[inner_select]):
            # A free selection of inner boards is all the boards which aren't already won.
            self.select = np.ones(TTT_SHAPE) - np.abs(self.wins)
        else:
            # Otherwise, the next board to play is defined by the two last axes of the move
            self.select = np.zeros(TTT_SHAPE)
            self.select[inner_select] = 1
        
        self.player *= -1
        self.turn += 1
        return 0 #No winner
        
        
    def winner(board):
        return 1 if UltimateTicTacToe.is_win(board==1) else -1 if UltimateTicTacToe.is_win(board==-1) else 0
    
    
    def is_win(board):
        return (np.all(board,axis=0).any() # 3 in a row horizontally/vertically
            or np.all(board,axis=1).any()
            or np.all(board.diagonal()) # 3 in a row on the diagonal
            or np.all(np.flipud(board).diagonal()))
    
    
    def legal_moves(self):
        moves = np.zeros(UTTT_SHAPE)
        outer_indices = self.select.nonzero()
        # The legal moves are all the empty squares in the inner boards permitted by the previous move
        moves[outer_indices] = self.board[outer_indices] == 0
        return moves

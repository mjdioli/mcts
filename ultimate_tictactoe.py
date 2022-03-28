import numpy as np

UTTT_SHAPE = (3,3,3,3)
TTT_SHAPE = (3,3)

class UltimateTicTacToe:
    
    
    def __init__(self, board=np.zeros(UTTT_SHAPE), select=np.ones(TTT_SHAPE), wins=np.zeros(TTT_SHAPE), player=1, turn=0):
        self.board = np.copy(board)
        self.select = np.copy(select)
        self.wins = np.copy(wins)
        self.player = player #x starts
        self.turn = turn
    
    
    def immutable_transition_function(self, action : tuple):
        game_copy = UltimateTicTacToe(self.board, self.select, self.wins, self.player, self.turn)
        winner = game_copy.mutable_transition_function(action)
        return game_copy, winner
    
    
    def mutable_transition_function(self, action : tuple) -> int:
        action = tuple(action)
        outer_select, inner_select = action[:2], action[2:]
        
        if (not self.select[outer_select]) or self.board[action]:
            raise Exception()
        
        self.board[action] = self.player
        
        if UltimateTicTacToe.winner(self.board[outer_select]):
            self.wins[outer_select] = self.player
            if (winner := UltimateTicTacToe.winner(self.wins)):
                return winner
        
        if UltimateTicTacToe.winner(self.board[inner_select]):
            self.select = np.ones(TTT_SHAPE) - np.abs(self.wins)
        else:
            self.select = np.zeros(TTT_SHAPE)
            self.select[inner_select] = 1
        self.player *= -1
        self.turn += 1
        return 0 #No winner
        
        
    def winner(board):
        return 1 if UltimateTicTacToe.is_win(board==1) else -1 if UltimateTicTacToe.is_win(board==-1) else 0
    
    
    def is_win(board):
        return (np.all(board,axis=0).any()
            or np.all(board,axis=1).any()
            or np.all(board.diagonal())
            or np.all(np.flipud(board).diagonal()))
    
    
    def legal_moves(self):
        moves = np.zeros(UTTT_SHAPE)
        outer_indices = self.select.nonzero()
        moves[outer_indices] = self.board[outer_indices] == 0
        return moves

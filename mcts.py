import math
from ultimate_tictactoe import UltimateTicTacToe, simulate

#https://blog.theofekfoundation.org/artificial-intelligence/2016/06/27/what-is-the-monte-carlo-tree-search/

class MCTSnode:
    
    
    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent
        self.hits = self.misses = self.trials = 0
    
    
    def choose_child(self):
        
        if self.children == None:
            self.children = self.get_children()
        
        if len(self.children) == 0:
            self.run_simulation()
        
        else:
            unexplored = [ child for child in self.children if child.trials == 0]
            
            if unexplored:
                random.choice(unexplored).run_simulation()
            else:
                best_child = self.children[0]
                best_potential = self.child_potential(best_child)
                
                idx = np.argmax([self.child_potential(child) for child in self.children])
                self.children[idx].choose_child()
    
    
    def child_potential(self, child):
        w = child.misses - child.hits
        n = child.trials
        t = self.trials
        return (w / n) + (2 * (math.log(t) / n))**0.5
    
    
    def run_simulation(self):
        self.backpropogate(simulate(self.state))
    
    
    def backpropogate(self, simulation):
        if simulation > 0:
            self.hits += 1
        elif simulation < 0:
            self.misses += 1
        
        self.trials += 1
        
        if self.parent != None:
            self.parent.backpropogate(-simulation)
    
    
    def get_children(self):
        return [MCTSnode(self.state.immutable_transition_function( move )[0], self) for move in self.state.legal_moves()]

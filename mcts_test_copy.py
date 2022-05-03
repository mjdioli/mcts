#!/usr/bin/env python
# coding: utf-8

# In[1]:


from mcts_borrowed import MCTS
from utt2 import UTTNode
from tqdm import tqdm


# In[2]:


X = MCTS(1, 1)
O = MCTS(1,-1, "norm")


# In[3]:


def play_game(x, o):
    board = UTTNode(current_player=1)
    #while not board.is_terminal():
    for i in range(100):
        # You can train as you go, or only at the beginning.
        # Here, we train as we go, doing fifty rollouts each turn.
        x.do_rollout(board)
        board = x.choose(board)
        if board.is_terminal():
            #print(board)
            break
        o.do_rollout(board)
        board = o.choose(board)
        if board.is_terminal():
            #print(board)
            break
    return board.reward()
    
    #print(board)
        
    #print(board)


# In[ ]:





# In[4]:


results = {"X": 0, "O": 0, "Tie": 0}
for i in tqdm(range(50)):
    result = play_game(X, O)
    #print("max: ", max(X.Q.values()), "\n",
    #"min: ", min(X.Q.values()))
    if result ==1:
        results["X"] +=1
    elif result == -1:
        results["O"] += 1
    else:
        results["Tie"]+=1


# In[ ]:


print(results)
#Play against random moves
#X-axis is games played and  y axis is average return versus random opponent


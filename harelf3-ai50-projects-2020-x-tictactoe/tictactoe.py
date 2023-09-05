
"""
Tic Tac Toe Player
"""

import math
from os import curdir
import random
import copy
from typing import MappingView 

X = "X"
O = "O"
EMPTY = None
perfect_action = []

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# works good #
def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_amount = 0
    o_amount = 0
    for row in board:
        for column in row:
            if column == X:
                x_amount = x_amount+1
            if column == O :
                o_amount = o_amount+1
            else:
                continue
    if x_amount == o_amount:
        return X
    if x_amount > o_amount:
        return O

# works good #
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in range(3) :
        for column in range(3):
            if board[row][column] == EMPTY:
                my_action =(row,column)
                actions.add(my_action)
    return actions

# works good #
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result = copy.deepcopy(board)
    i =action[0]
    j =action[1]
    result[i][j]=player(board)
    return result
    

# works good #
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board :
        if row[0] == X or row[0] == O :
            if row[0] == row[1] == row[2]:
                return row[0]
    for i in range(3):
        if board[0][i] == X or board[0][i] == O :
            if board[0][i] == board[1][i] == board[2][i]:
                return board[0][i]
    if board[1][1] == X or board[1][1] == O :
        if board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        if board[2][0] == board[1][1] == board[0][2]:
            return board[2][0]
    return None


# works good #
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    for row in board :
        if row[0] == X or row[0] == O :
            if row[0] == row[1] == row[2]:
                return True
    for i in range(3):
        if board[0][i] == X or board[0][i] == O :
            if board[0][i] == board[1][i] == board[2][i]:
               return True
    if board[1][1] == X or board[1][1] == O :
        if board[0][0] == board[1][1] == board[2][2]:
            return True
        if board[2][0] == board[1][1] == board[0][2]:
            return True
    for row in board :
        for column in row:
            if column == EMPTY:
                return False
    return True 
    
    

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result == None:
        return 0
    if result == O:
        return -1
    if result == X:
        return 1
    
    
    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return utility(board)
    if player(board) == X :
        print(Max_Value(board))
        value, move =  Max_Value(board)
        return move
    else :
        print(Min_Value(board))
        value, move = Min_Value(board)
        return move
    

def Max_Value(board):
    if terminal(board):
        return utility(board),None
    v = -20
    move = None
    for action in actions(board):
        temp,z = Min_Value(result(board,action))
        if temp > v:
            v =temp
            move = action
            if temp ==1:
                return v ,move
    return v , move


def Min_Value(board):
    v = 20
    move = None
    if terminal(board):
       return utility(board),None
    for action in actions(board):
        temp,z = Max_Value(result(board,action))
        if temp < v:
            v= temp
            move =action
            if temp == -1:
                return v, move
    return v ,move
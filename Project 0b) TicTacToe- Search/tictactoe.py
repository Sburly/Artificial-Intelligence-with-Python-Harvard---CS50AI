"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    spreaded = [cell for li in board for cell in li]
    if spreaded.count(EMPTY) == 0:
        return "Game Over"
    return X if spreaded.count(X) == spreaded.count(O) else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == EMPTY} if [cell for li in board for cell in li].count(EMPTY) != 0 else "Game Over"


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] == EMPTY:
        new_board = copy.deepcopy(board)
        new_board[action[0]][action[1]] = player(board)
        return new_board
    else:
        raise NameError('Invalid action')


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    vertical = []
    for i in range(len(board)):
        col = []
        for j in range(len(board[0])): 
            col.append(board[j][i])
        vertical.append(col)
    combinations = [*board, *vertical, [board[i][i] for i in range(len(board))], [board[i][len(board) - i - 1] for i in range(len(board))]]
    for player in [X, O]:
        for comb in combinations:
            if comb.count(player) == 3: 
                return player
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return True if winner(board) != None or player(board) not in [X, O] else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    utility = {X: 1, O: -1}
    return utility[winner(board)] if winner(board) != None else 0


def max_value(board, alpha, beta, depth):
    if terminal(board):
        return utility(board) / depth, None
    v = float("-inf")
    best = None
    for action in actions(board):
        value, a = min_value(result(board, action), alpha, beta, depth+1)
        # We increase the depth at each iteration so the utility value can be tailored based on that
        if value > v:
            v = value
            best = action
        alpha = max(alpha, v)
        if v >= beta: # If we find a value that is higher or equal than beta, then we directly return that value
            return v, best
    return v, best


def min_value(board, alpha, beta, depth):
    if terminal(board):
        return utility(board) / depth, None
    v = float("inf")
    best = None
    for action in actions(board):
        value, a = max_value(result(board, action), alpha, beta, depth+1)
        # We increase the depth at each iteration so the utility value can be tailored based on that
        if value < v:
            v = value
            best = action
        beta = min(beta, v)
        if v <= alpha: # If we find a value that is lower or equal than alpha, then we directly return that value
            return v, best
    return v, best


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    depth = 1 # We not only want to calculate the winning move but also the fastest one
    # The utility of the terminal board is divided by the depth. This way, the greater the depth, the smaller the value. Values are not just 1, -1 or 0 anymore.
    initial_alpha = float("-inf")
    initial_beta = float("inf")
    return (max_value(board, initial_alpha, initial_beta, depth))[1] if player(board) == X else (min_value(board, initial_alpha, initial_beta, depth))[1]
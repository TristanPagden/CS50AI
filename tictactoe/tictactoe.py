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
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_x = 0
    num_o = 0

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == X:
                num_x += 1
            elif board[i][j] == O:
                num_o += 1

    if num_x > num_o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        num_x = 0
        num_o = 0
        for col in row:
            if col == EMPTY:
                continue
            elif col == X:
                num_x += 1
            else:
                num_o += 1
        if num_x == 3:
            return X
        elif num_o == 3:
            return O

    for col in range(len(board)):
        num_x = 0
        num_o = 0
        for row in range(len(board[col])):
            if board[row][col] == EMPTY:
                continue
            elif board[row][col] == X:
                num_x += 1
            else:
                num_o += 1
        if num_x == 3:
            return X
        elif num_o == 3:
            return O

    num_x = 0
    num_o = 0
    for i in range(len(board)):
        if board[i][i] == EMPTY:
            continue
        elif board[i][i] == X:
            num_x += 1
        else:
            num_o += 1
    if num_x == 3:
        return X
    elif num_o == 3:
        return O

    num_x = 0
    num_o = 0
    for i in range(len(board)):
        if board[i][len(board) - 1 - i] == EMPTY:
            continue
        elif board[i][len(board) - 1 - i] == X:
            num_x += 1
        else:
            num_o += 1
    if num_x == 3:
        return X
    elif num_o == 3:
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    else:
        for row in board:
            for col in row:
                if col == EMPTY:
                    return False
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        value, optimal_action = max_value(board)
        return optimal_action
    else:
        value, optimal_action = min_value(board)
        return optimal_action

    raise NotImplementedError


def max_value(board):
    if terminal(board):
        return utility(board), None

    v = float("-inf")
    optimal_action = None
    for action in actions(board):
        min_value_result, _ = min_value(result(board, action))
        print(min_value_result)
        if min_value_result > v:
            v = min_value_result
            optimal_action = action
            if v == 1:
                return v, optimal_action

    return v, optimal_action


def min_value(board):
    if terminal(board):
        return utility(board), None

    v = float("inf")
    optimal_action = None
    for action in actions(board):
        max_value_result, _ = max_value(result(board, action))
        print(max_value_result)
        if max_value_result < v:
            v = max_value_result
            optimal_action = action
            if v == -1:
                return v, optimal_action

    return v, optimal_action

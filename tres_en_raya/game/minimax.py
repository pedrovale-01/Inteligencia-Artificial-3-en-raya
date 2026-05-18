import math
from game.logic import player, actions, result, terminal, utility, X


def minimax(board):
    # Devuelve la mejor jugada para el jugador actual
    if terminal(board):
        return None
    if player(board) == X:
        return max_value(board, -math.inf, math.inf)[1]
    return min_value(board, -math.inf, math.inf)[1]


def max_value(board, alpha, beta):
    # X quiere el valor más alto posible
    if terminal(board):
        return utility(board), None
    v, best = -math.inf, None
    for action in actions(board):
        score = min_value(result(board, action), alpha, beta)[0]
        if score > v:
            v, best = score, action
        alpha = max(alpha, v)
        if alpha >= beta:
            break
    return v, best


def min_value(board, alpha, beta):
    # O quiere el valor más bajo posible
    if terminal(board):
        return utility(board), None
    v, best = math.inf, None
    for action in actions(board):
        score = max_value(result(board, action), alpha, beta)[0]
        if score < v:
            v, best = score, action
        beta = min(beta, v)
        if alpha >= beta:
            break
    return v, best

X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [[EMPTY]*3 for _ in range(3)]


def player(board):
    # Quien tenga menos fichas, mueve
    xs = sum(row.count(X) for row in board)
    os = sum(row.count(O) for row in board)
    return X if xs == os else O


def actions(board):
    # Devuelve las celdas vacías
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    # Copia el tablero y pone la ficha en la celda elegida
    i, j = action
    new = [row[:] for row in board]
    new[i][j] = player(board)
    return new


def winner(board):
    # Revisa las 8 líneas posibles (filas, columnas, diagonales)
    lines = (
        [board[r] for r in range(3)] +
        [[board[r][c] for r in range(3)] for c in range(3)] +
        [[board[i][i] for i in range(3)], [board[i][2-i] for i in range(3)]]
    )
    for line in lines:
        if line[0] and line[0] == line[1] == line[2]:
            return line[0]
    return None


def terminal(board):
    # El juego terminó si hay ganador o no quedan celdas
    return winner(board) is not None or not actions(board)


def utility(board):
    # +1 gana X, -1 gana O, 0 empate
    w = winner(board)
    return 1 if w == X else -1 if w == O else 0

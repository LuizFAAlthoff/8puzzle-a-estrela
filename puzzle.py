GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def is_solvable(state):
    """Verifica se o estado tem solução contando inversões.

    Para o 8-puzzle com solução fixa, o número de inversões deve ser par.
    Uma inversão ocorre quando uma peça de valor maior aparece antes de
    uma de valor menor na leitura linear do tabuleiro (ignorando o espaço).
    """
    tiles = [t for t in state if t != 0]
    inversions = sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )
    return inversions % 2 == 0


def get_neighbors(state):
    """Retorna lista de (novo_estado, movimento) a partir do estado atual.

    Os movimentos descrevem para onde o espaço em branco se desloca.
    """
    idx = state.index(0)
    row, col = divmod(idx, 3)
    directions = [
        (-1, 0, "cima"),
        ( 1, 0, "baixo"),
        ( 0,-1, "esquerda"),
        ( 0, 1, "direita"),
    ]
    neighbors = []
    for dr, dc, move in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_idx = nr * 3 + nc
            lst = list(state)
            lst[idx], lst[new_idx] = lst[new_idx], lst[idx]
            neighbors.append((tuple(lst), move))
    return neighbors


def print_board(state):
    """Imprime o tabuleiro formatado."""
    for i in range(0, 9, 3):
        row = [str(state[i + j]) if state[i + j] != 0 else "_" for j in range(3)]
        print("  " + " ".join(row))
    print()

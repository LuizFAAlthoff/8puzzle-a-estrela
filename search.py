import time

from puzzle import GOAL, get_neighbors


def _reconstruct_path(parent, goal):
    path = []
    cur = goal
    while parent[cur] is not None:
        par, move = parent[cur]
        path.append(move)
        cur = par
    path.reverse()
    return path


def _insert_sorted(frontier, item):
    """Insere item mantendo a lista frontier ordenada pelo f-value (primeiro elemento).
    
    Usa busca binária para encontrar a posição correta e insere o elemento,
    mantendo a ordem de prioridade da fila.
    """
    left, right = 0, len(frontier)
    while left < right:
        mid = (left + right) // 2
        if frontier[mid] < item:
            left = mid + 1
        else:
            right = mid
    frontier.insert(left, item)


def a_star(start, heuristic, max_nodes=500_000):
    """Busca A* (ou Custo Uniforme quando heuristic retorna 0).

        Estrutura da fronteira
        ----------------------
        Lista ordenada com entradas (f, g, counter, state), onde:
            f       = g + h  →  custo estimado total
            g       = custo real acumulado do início até state
            counter = desempata entradas com mesmo f sem comparar tuplas de estado
            state   = tupla representando o tabuleiro

    Verificações antes de adicionar um vizinho à fronteira
    ------------------------------------------------------
    1. Se o vizinho já está no conjunto fechado (closed) → descarta.
       Nodos no fechado já foram expandidos com custo ótimo.
    2. Se já existe um g registrado para o vizinho com custo menor
       ou igual ao novo g → descarta. Já há um caminho mais barato
       conhecido (ou igual) para esse estado na fronteira.

    Parâmetros
    ----------
    start       : tupla com o estado inicial (9 inteiros)
    heuristic   : função h(state) -> int
    max_nodes   : limite de segurança para evitar loop infinito

    Retorno
    -------
    Dicionário com os resultados ou None se não houver solução.
    """
    counter = 0
    frontier = [(heuristic(start), 0, counter, start)]

    closed = set()
    g_costs = {start: 0}
    parent = {start: None}  # state -> (parent_state, move) | None

    max_frontier_size = 1
    visited_count = 0
    start_time = time.time()

    while True:
        if not frontier:
            return None

        f, g, _, state = frontier.pop(0)

        if state in closed:
            continue

        closed.add(state)
        visited_count += 1

        if visited_count > max_nodes:
            return None

        if state == GOAL:
            elapsed = time.time() - start_time
            return {
                "path":              _reconstruct_path(parent, GOAL),
                "visited_count":     visited_count,
                "time_seconds":      round(elapsed, 6),
                "max_frontier_size": max_frontier_size,
                "frontier_at_end":   [list(item[3]) for item in frontier],
                "visited_at_end":    [list(s) for s in closed],
            }

        for neighbor, move in get_neighbors(state):
            if neighbor in closed:
                continue
            new_g = g + 1
            # Só enfileira se encontrou caminho mais barato (ou inédito)
            if neighbor not in g_costs or g_costs[neighbor] > new_g:
                g_costs[neighbor] = new_g
                parent[neighbor] = (state, move)
                counter += 1
                _insert_sorted(frontier, (new_g + heuristic(neighbor), new_g, counter, neighbor))
                max_frontier_size = max(max_frontier_size, len(frontier))

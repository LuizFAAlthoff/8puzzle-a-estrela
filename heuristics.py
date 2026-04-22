from puzzle import GOAL

# Posição-objetivo de cada peça: tile -> (linha, coluna)
GOAL_POS = {tile: divmod(i, 3) for i, tile in enumerate(GOAL)}


def h_zero(state):
    """Custo Uniforme — sem heurística (h = 0).

    Degenera o A* em busca de custo uniforme (Dijkstra). Garante
    solução ótima, mas expande todos os nodos com custo ≤ solução.
    """
    return 0


def h_inadmissivel(state):
    """Heurística NÃO admissível — peças fora do lugar × 3.

    Multiplica por 3 faz a estimativa superar o custo real, violando
    a condição de admissibilidade. O A* pode encontrar caminhos
    sub-ótimos, mas geralmente expande muito menos nodos.
    """
    return sum(3 for i, t in enumerate(state) if t != 0 and t != GOAL[i])


def h_pecas_fora(state):
    """Heurística admissível simples — número de peças fora do lugar.

    Admissível porque cada peça fora de lugar precisa de ao menos
    1 movimento para chegar à posição correta. Nunca superestima.
    """
    return sum(1 for i, t in enumerate(state) if t != 0 and t != GOAL[i])


def h_manhattan(state):
    """Heurística admissível precisa — soma das distâncias de Manhattan.

    Para cada peça, calcula a distância |Δlinha| + |Δcoluna| até sua
    posição-objetivo. Admissível pois ignora colisões entre peças
    (cada peça se move de forma independente no cálculo). Domina
    h_pecas_fora: h_manhattan(s) ≥ h_pecas_fora(s) para todo estado s.
    """
    total = 0
    for i, tile in enumerate(state):
        if tile != 0:
            cr, cc = divmod(i, 3)
            gr, gc = GOAL_POS[tile]
            total += abs(cr - gr) + abs(cc - gc)
    return total


ALGORITHMS = {
    1: ("Custo Uniforme",           h_zero),
    2: ("A* Inadmissível (×3)",     h_inadmissivel),
    3: ("A* Peças Fora do Lugar",   h_pecas_fora),
    4: ("A* Manhattan",             h_manhattan),
}

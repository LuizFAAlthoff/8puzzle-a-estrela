from puzzle import ESTADO_OBJETIVO

# Posição-objetivo de cada peça: peça -> (linha, coluna)
POSICOES_OBJETIVO = {peca: divmod(indice, 3) for indice, peca in enumerate(ESTADO_OBJETIVO)}


def heuristica_nula(estado):
    """Custo Uniforme — sem heurística (h = 0).

    Degenera o A* em busca de custo uniforme (Dijkstra). Garante
    solução ótima, mas expande todos os nodos com custo ≤ solução.
    """
    return 0


def heuristica_inadmissivel(estado):
    """Heurística NÃO admissível — peças fora + Manhattan.

    Soma duas estimativas admissíveis para forçar superestimação em
    diversos estados. Serve para comparar desempenho vs. qualidade.
    """
    return heuristica_pecas_fora_lugar(estado) + heuristica_manhattan(estado)


def heuristica_pecas_fora_lugar(estado):
    """Heurística admissível simples — número de peças fora do lugar.

    Admissível porque cada peça fora de lugar precisa de ao menos
    1 movimento para chegar à posição correta. Nunca superestima.
    """
    return sum(1 for indice, peca in enumerate(estado) if peca != 0 and peca != ESTADO_OBJETIVO[indice])


def heuristica_manhattan(estado):
    """Heurística admissível precisa — soma das distâncias de Manhattan.

    Para cada peça, calcula a distância |Δlinha| + |Δcoluna| até sua
    posição-objetivo. Admissível pois ignora colisões entre peças
    (cada peça se move de forma independente no cálculo). Domina
    heuristica_pecas_fora_lugar: heuristica_manhattan(s) ≥ heuristica_pecas_fora_lugar(s) para todo estado s.
    """
    total = 0
    for indice, peca in enumerate(estado):
        if peca != 0:
            linha_atual, coluna_atual = divmod(indice, 3)
            linha_objetivo, coluna_objetivo = POSICOES_OBJETIVO[peca]
            total += abs(linha_atual - linha_objetivo) + abs(coluna_atual - coluna_objetivo)
    return total


ALGORITMOS = {
    1: ("Custo Uniforme",           heuristica_nula),
    2: ("A* Peças Fora do Lugar",   heuristica_pecas_fora_lugar),
    3: ("A* Manhattan",             heuristica_manhattan),
    4: ("A* Não Admissível (Soma)", heuristica_inadmissivel),
}

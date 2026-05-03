from puzzle import ESTADO_OBJETIVO

POSICOES_OBJETIVO = {peca: divmod(indice, 3) for indice, peca in enumerate(ESTADO_OBJETIVO)}


def heuristica_nula(estado):
    return 0


def heuristica_inadmissivel(estado):
    return heuristica_pecas_fora_lugar(estado) + heuristica_manhattan(estado)


def heuristica_pecas_fora_lugar(estado):
    return sum(1 for indice, peca in enumerate(estado) if peca != 0 and peca != ESTADO_OBJETIVO[indice])


def heuristica_manhattan(estado):
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

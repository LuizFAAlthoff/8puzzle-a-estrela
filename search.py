import time

from puzzle import ESTADO_OBJETIVO, obter_vizinhos


def reconstruir_caminho(predecessores, estado_objetivo):
    caminho = []
    estado_atual = estado_objetivo
    while predecessores[estado_atual] is not None:
        estado_pai, movimento = predecessores[estado_atual]
        caminho.append(movimento)
        estado_atual = estado_pai
    caminho.reverse()
    return caminho


def inserir_ordenado(fronteira, item):
    esquerda, direita = 0, len(fronteira)
    while esquerda < direita:
        meio = (esquerda + direita) // 2
        if fronteira[meio] < item:
            esquerda = meio + 1
        else:
            direita = meio
    fronteira.insert(esquerda, item)


def busca_a_estrela(estado_inicial, heuristica, max_nodos=500_000):
    fronteira = [(heuristica(estado_inicial), 0, estado_inicial)]

    fechados = set()
    custos_g = {estado_inicial: 0}
    predecessores = {estado_inicial: None}

    maior_tamanho_fronteira = 1
    quantidade_visitados = 0
    tempo_inicial = time.time()

    while True:
        if not fronteira:
            return None

        _, custo_acumulado, estado_atual = fronteira.pop(0)

        if estado_atual in fechados:
            continue

        fechados.add(estado_atual)
        quantidade_visitados += 1

        if quantidade_visitados > max_nodos:
            return None

        if estado_atual == ESTADO_OBJETIVO:
            tempo_decorrido = time.time() - tempo_inicial
            return {
                "caminho": reconstruir_caminho(predecessores, ESTADO_OBJETIVO),
                "quantidade_visitados": quantidade_visitados,
                "tempo_em_segundos": round(tempo_decorrido, 6),
                "maior_tamanho_fronteira": maior_tamanho_fronteira,
                "fronteira_final": [list(item[2]) for item in fronteira],
                "visitados_finais": [list(estado) for estado in fechados],
            }

        for vizinho, movimento in obter_vizinhos(estado_atual):
            if vizinho in fechados:
                continue

            novo_custo_g = custo_acumulado + 1
            if vizinho not in custos_g or custos_g[vizinho] > novo_custo_g:
                custos_g[vizinho] = novo_custo_g
                predecessores[vizinho] = (estado_atual, movimento)
                inserir_ordenado(
                    fronteira,
                    (novo_custo_g + heuristica(vizinho), novo_custo_g, vizinho),
                )
                maior_tamanho_fronteira = max(maior_tamanho_fronteira, len(fronteira))

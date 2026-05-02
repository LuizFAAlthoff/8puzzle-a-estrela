import time

from puzzle import ESTADO_OBJETIVO, obter_vizinhos


def reconstruir_caminho(predecessores, estado_objetivo):
    caminho = []
    atual = estado_objetivo
    while predecessores[atual] is not None:
        estado_anterior, movimento = predecessores[atual]
        caminho.append(movimento)
        atual = estado_anterior
    caminho.reverse()
    return caminho


def inserir_ordenado(fronteira, item):
    """Insere item mantendo a lista fronteira ordenada pelo custo estimado total."""
    esquerda, direita = 0, len(fronteira)
    while esquerda < direita:
        meio = (esquerda + direita) // 2
        if fronteira[meio] < item:
            esquerda = meio + 1
        else:
            direita = meio
    fronteira.insert(esquerda, item)


def busca_a_estrela(estado_inicial, heuristica, max_nodos=500_000):
    """Busca A* (ou Custo Uniforme quando heuristica retorna 0).

    Estrutura da fronteira
    ----------------------
    Lista ordenada com entradas (f, g, contador, estado), onde:
        f        = g + h  -> custo estimado total
        g        = custo real acumulado do início até o estado
        contador = desempata entradas com mesmo f sem comparar tuplas de estado
        estado   = tupla representando o tabuleiro

    Verificações antes de adicionar um vizinho à fronteira
    ------------------------------------------------------
    1. Se o vizinho já está no conjunto fechado (fechados) -> descarta.
    2. Se já existe um g registrado para o vizinho com custo menor ou igual
       ao novo g -> descarta.

    Retorna um dicionário com os resultados ou None se não houver solução.
    """
    contador = 0
    fronteira = [(heuristica(estado_inicial), 0, contador, estado_inicial)]

    fechados = set()
    custos_g = {estado_inicial: 0}
    predecessores = {estado_inicial: None}

    maior_tamanho_fronteira = 1
    quantidade_visitados = 0
    tempo_inicial = time.time()

    while True:
        if not fronteira:
            return None

        custo_estimado_total, custo_acumulado, _, estado_atual = fronteira.pop(0)

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
                "fronteira_final": [list(item[3]) for item in fronteira],
                "visitados_finais": [list(estado) for estado in fechados],
            }

        for vizinho, movimento in obter_vizinhos(estado_atual):
            if vizinho in fechados:
                continue

            novo_custo_g = custo_acumulado + 1

            if vizinho not in custos_g or custos_g[vizinho] > novo_custo_g:
                custos_g[vizinho] = novo_custo_g
                predecessores[vizinho] = (estado_atual, movimento)
                contador += 1
                inserir_ordenado(fronteira, (novo_custo_g + heuristica(vizinho), novo_custo_g, contador, vizinho))
                maior_tamanho_fronteira = max(maior_tamanho_fronteira, len(fronteira))

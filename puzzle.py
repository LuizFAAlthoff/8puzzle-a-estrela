ESTADO_OBJETIVO = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def e_resolvivel(estado):
    """Verifica se o estado tem solução contando inversões.

    Para o 8-puzzle com solução fixa, o número de inversões deve ser par.
    Uma inversão ocorre quando uma peça de valor maior aparece antes de
    uma de valor menor na leitura linear do tabuleiro (ignorando o espaço).
    """
    pecas = [peca for peca in estado if peca != 0]
    inversoes = sum(
        1
        for indice_atual in range(len(pecas))
        for indice_posterior in range(indice_atual + 1, len(pecas))
        if pecas[indice_atual] > pecas[indice_posterior]
    )
    return inversoes % 2 == 0


def obter_vizinhos(estado):
    """Retorna lista de (novo_estado, movimento) a partir do estado atual.

    Os movimentos descrevem para onde o espaço em branco se desloca.
    """
    indice_do_espaco = estado.index(0)
    linha, coluna = divmod(indice_do_espaco, 3)
    direcoes = [
        (-1, 0, "cima"),
        (1, 0, "baixo"),
        (0, -1, "esquerda"),
        (0, 1, "direita"),
    ]
    vizinhos = []
    for deslocamento_linha, deslocamento_coluna, movimento in direcoes:
        nova_linha, nova_coluna = linha + deslocamento_linha, coluna + deslocamento_coluna
        if 0 <= nova_linha < 3 and 0 <= nova_coluna < 3:
            novo_indice = nova_linha * 3 + nova_coluna
            estado_lista = list(estado)
            estado_lista[indice_do_espaco], estado_lista[novo_indice] = estado_lista[novo_indice], estado_lista[indice_do_espaco]
            vizinhos.append((tuple(estado_lista), movimento))
    return vizinhos


def imprimir_tabuleiro(estado):
    """Imprime o tabuleiro formatado."""
    for indice in range(0, 9, 3):
        linha = [str(estado[indice + deslocamento]) if estado[indice + deslocamento] != 0 else "_" for deslocamento in range(3)]
        print("  " + " ".join(linha))
    print()

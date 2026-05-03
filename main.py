import json
import os
import random
import re
import sys
import unicodedata

from heuristics import ALGORITMOS
from puzzle import e_resolvivel, imprimir_tabuleiro
from search import busca_a_estrela

PASTA_SAIDA = os.path.join(os.path.dirname(__file__), "output")
ESTADO_OBJETIVO = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def aplicar_movimentos(estado_inicial, movimentos):
    estado = list(estado_inicial)
    for movimento in movimentos:
        indice_do_espaco = estado.index(0)
        linha, coluna = divmod(indice_do_espaco, 3)

        if movimento == "left" and coluna > 0:
            indice_troca = indice_do_espaco - 1
        elif movimento == "right" and coluna < 2:
            indice_troca = indice_do_espaco + 1
        elif movimento == "up" and linha > 0:
            indice_troca = indice_do_espaco - 3
        elif movimento == "down" and linha < 2:
            indice_troca = indice_do_espaco + 3
        else:
            raise ValueError(f"Movimento inválido '{movimento}' para o estado {tuple(estado)}")

        estado[indice_do_espaco], estado[indice_troca] = estado[indice_troca], estado[indice_do_espaco]

    return tuple(estado)


def gerar_estado_embaralhado(movimentos):
    return aplicar_movimentos(ESTADO_OBJETIVO, movimentos)


def obter_casos_padrao():
    return [
        ("facil_1", gerar_estado_embaralhado(["left", "up", "left"])),
        ("facil_2", gerar_estado_embaralhado(["up", "left", "down", "right"])),
        ("medio_1", gerar_estado_embaralhado(["left", "up", "left", "down", "right", "up"])),
        ("medio_2", gerar_estado_embaralhado(["up", "left", "down", "left", "up", "right"])),
        ("dificil_1", gerar_estado_aleatorio()),
        ("dificil_2", gerar_estado_aleatorio())
    ]


def gerar_estado_aleatorio():
    while True:
        estado = list(range(9))
        random.shuffle(estado)
        estado_inicial = tuple(estado)
        if estado_inicial != ESTADO_OBJETIVO and e_resolvivel(estado_inicial):
            return estado_inicial


def salvar_saida(nome_caso, identificador_algoritmo, resultado):
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    # Normaliza e remove caracteres inválidos para nomes de arquivo no Windows.
    nome_algoritmo = ALGORITMOS[identificador_algoritmo][0].lower().replace("×", "x")
    nome_algoritmo = unicodedata.normalize("NFKD", nome_algoritmo).encode("ascii", "ignore").decode("ascii")
    identificador_amigavel = re.sub(r"[^a-z0-9]+", "_", nome_algoritmo).strip("_")

    nome_arquivo = os.path.join(PASTA_SAIDA, f"{nome_caso}_{identificador_algoritmo}_{identificador_amigavel}.json")
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo_saida:
        json.dump(
            {
                "fronteira_final": resultado["fronteira_final"],
                "visitados_finais": resultado["visitados_finais"],
            },
            arquivo_saida,
            indent=2,
        )
    return nome_arquivo


def executar_algoritmo(estado_inicial, identificador_algoritmo, nome_caso):
    nome_algoritmo, heuristica = ALGORITMOS[identificador_algoritmo]
    print(f"\n  [{identificador_algoritmo}] {nome_algoritmo}")

    resultado = busca_a_estrela(estado_inicial, heuristica)

    if resultado is None:
        print("      Sem solução (limite de nodos atingido).")
        return None

    tamanho_caminho = len(resultado["caminho"])
    print(f"      Caminho ({tamanho_caminho} passos): {' -> '.join(resultado['caminho'])}")
    print(f"      a) Nodos visitados : {resultado['quantidade_visitados']}")
    print(f"      b) Tamanho caminho : {tamanho_caminho}")
    print(f"      c) Tempo execução  : {resultado['tempo_em_segundos']}s")
    print(f"      d) Maior fronteira : {resultado['maior_tamanho_fronteira']}")
    nome_arquivo = salvar_saida(nome_caso, identificador_algoritmo, resultado)
    print(f"      e) Arquivo gerado  : {nome_arquivo}")

    return resultado


def imprimir_tabela_comparativa(nome_caso, resumo):
    print(f"\n  {'=' * 72}")
    print(f"  TABELA COMPARATIVA — {nome_caso.upper()}")
    print(f"  {'Algoritmo':<32} {'Visitados':>10} {'Caminho':>8} {'Tempo(s)':>11} {'MaxFront':>10}")
    print(f"  {'-' * 72}")
    for linha in resumo:
        print(
            f"  {linha['nome']:<32} {linha['visitados']:>10} {linha['caminho']:>8}"
            f" {linha['tempo']:>11.6f} {linha['max_fronteira']:>10}"
        )


def executar_caso(estado_inicial, nome_caso, identificadores_algoritmos):
    print(f"\n{'#' * 60}")
    print(f"CASO: {nome_caso.upper()}")
    print("Estado inicial:")
    imprimir_tabuleiro(estado_inicial)

    if not e_resolvivel(estado_inicial):
        print("  Este estado não possui solução.")
        return

    resumo = []
    for identificador_algoritmo in identificadores_algoritmos:
        resultado = executar_algoritmo(estado_inicial, identificador_algoritmo, nome_caso)
        if resultado:
            nome_algoritmo, _ = ALGORITMOS[identificador_algoritmo]
            resumo.append({
                "nome":         nome_algoritmo,
                "visitados":    resultado["quantidade_visitados"],
                "caminho":      len(resultado["caminho"]),
                "tempo":        resultado["tempo_em_segundos"],
                "max_fronteira": resultado["maior_tamanho_fronteira"],
            })

    if len(resumo) > 1:
        imprimir_tabela_comparativa(nome_caso, resumo)


def interpretar_argumentos():
    argumentos = sys.argv[1:]

    if not argumentos:
        return None  # usa casos predefinidos

    # Primeiro argumento: tabuleiro
    try:
        estado_inicial = tuple(int(valor) for valor in argumentos[0].split())
        assert len(estado_inicial) == 9 and sorted(estado_inicial) == list(range(9))
    except (ValueError, AssertionError):
        print("Erro: tabuleiro inválido.")
        print("Esperado: 9 números de 0 a 8 separados por espaço.")
        print('Exemplo:  python main.py "7 2 4 5 0 6 8 3 1"')
        sys.exit(1)

    # Segundo argumento opcional: número do algoritmo (1-4) ou "todos"
    if len(argumentos) >= 2:
        if argumentos[1].lower() in ("todos", "all"):
            identificadores_algoritmos = list(ALGORITMOS.keys())
        elif argumentos[1].isdigit() and int(argumentos[1]) in ALGORITMOS:
            identificadores_algoritmos = [int(argumentos[1])]
        else:
            print(f"Erro: algoritmo '{argumentos[1]}' inválido. Escolha entre 1, 2, 3, 4 ou 'todos'.")
            sys.exit(1)
    else:
        identificadores_algoritmos = list(ALGORITMOS.keys())

    return estado_inicial, identificadores_algoritmos, "custom"


if __name__ == "__main__":
    resultado_interpretacao = interpretar_argumentos()

    if resultado_interpretacao is None:
        for nome_caso, estado_inicial in obter_casos_padrao():
            executar_caso(estado_inicial, nome_caso, list(ALGORITMOS.keys()))
    else:
        estado_inicial, identificadores_algoritmos, nome_caso = resultado_interpretacao
        executar_caso(estado_inicial, nome_caso, identificadores_algoritmos)

"""8-Puzzle — Busca A* (Trabalho Prático 1 — Sistemas Inteligentes)

Uso
---
  # Roda todos os algoritmos em um estado e exibe tabela comparativa:
  python main.py "7 2 4 5 0 6 8 3 1"

  # Roda apenas um algoritmo específico (1-4):
  python main.py "7 2 4 5 0 6 8 3 1" 4

  # Roda os casos de teste predefinidos (fácil, médio, difícil):
  python main.py

Algoritmos disponíveis
----------------------
  1 — Custo Uniforme (sem heurística)
  2 — A* com heurística não admissível (peças fora × 3)
  3 — A* com heurística admissível simples (peças fora do lugar)
  4 — A* com heurística admissível precisa (distância Manhattan)
"""

import json
import os
import sys

from heuristics import ALGORITHMS
from puzzle import is_solvable, print_board
from search import a_star

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Casos predefinidos para comparativo
PREDEFINED_CASES = {
    "facil":   (1, 2, 3, 4, 5, 6, 7, 0, 8),  # 1 movimento
    "medio":   (4, 1, 0, 2, 5, 3, 7, 8, 6),  # 8 movimentos
    "dificil": (7, 2, 4, 5, 0, 6, 8, 3, 1),  # 20 movimentos
}


def save_output(case_name, alg_id, result):
    """Salva fronteira e visitados em arquivo JSON na pasta output/."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    alg_slug = ALGORITHMS[alg_id][0].lower().replace(" ", "_").replace("(", "").replace(")", "").replace("×", "x")
    filename = os.path.join(OUTPUT_DIR, f"{case_name}_{alg_id}_{alg_slug}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            {
                "frontier_at_end": result["frontier_at_end"],
                "visited_at_end":  result["visited_at_end"],
            },
            f,
            indent=2,
        )
    return filename


def run_algorithm(start, alg_id, case_name):
    """Executa um algoritmo, imprime resultados e salva o arquivo de saída."""
    alg_name, heuristic = ALGORITHMS[alg_id]
    print(f"\n  [{alg_id}] {alg_name}")

    result = a_star(start, heuristic)

    if result is None:
        print("      Sem solução (limite de nodos atingido).")
        return None

    path_length = len(result["path"])
    print(f"      Caminho ({path_length} passos): {' -> '.join(result['path'])}")
    print(f"      a) Nodos visitados : {result['visited_count']}")
    print(f"      b) Tamanho caminho : {path_length}")
    print(f"      c) Tempo execução  : {result['time_seconds']}s")
    print(f"      d) Maior fronteira : {result['max_frontier_size']}")
    filename = save_output(case_name, alg_id, result)
    print(f"      e) Arquivo gerado  : {filename}")

    return result


def print_comparison_table(case_name, summary):
    """Imprime tabela comparativa dos algoritmos executados."""
    print(f"\n  {'=' * 72}")
    print(f"  TABELA COMPARATIVA — {case_name.upper()}")
    print(f"  {'Algoritmo':<32} {'Visitados':>10} {'Caminho':>8} {'Tempo(s)':>11} {'MaxFront':>10}")
    print(f"  {'-' * 72}")
    for row in summary:
        print(
            f"  {row['nome']:<32} {row['visitados']:>10} {row['caminho']:>8}"
            f" {row['tempo']:>11.6f} {row['max_fronteira']:>10}"
        )


def run_case(start, case_name, alg_ids):
    """Executa os algoritmos selecionados para um estado inicial."""
    print(f"\n{'#' * 60}")
    print(f"CASO: {case_name.upper()}")
    print("Estado inicial:")
    print_board(start)

    if not is_solvable(start):
        print("  Este estado não possui solução.")
        return

    summary = []
    for alg_id in alg_ids:
        result = run_algorithm(start, alg_id, case_name)
        if result:
            alg_name, _ = ALGORITHMS[alg_id]
            summary.append({
                "nome":         alg_name,
                "visitados":    result["visited_count"],
                "caminho":      len(result["path"]),
                "tempo":        result["time_seconds"],
                "max_fronteira": result["max_frontier_size"],
            })

    if len(summary) > 1:
        print_comparison_table(case_name, summary)


def parse_args():
    """Interpreta os argumentos da linha de comando.

    Retorna (start, alg_ids, case_name) ou usa casos predefinidos.
    """
    args = sys.argv[1:]

    if not args:
        return None  # usa casos predefinidos

    # Primeiro argumento: tabuleiro
    try:
        start = tuple(int(x) for x in args[0].split())
        assert len(start) == 9 and sorted(start) == list(range(9))
    except (ValueError, AssertionError):
        print("Erro: tabuleiro inválido.")
        print("Esperado: 9 números de 0 a 8 separados por espaço.")
        print('Exemplo:  python main.py "7 2 4 5 0 6 8 3 1"')
        sys.exit(1)

    # Segundo argumento opcional: número do algoritmo (1-4) ou "todos"
    if len(args) >= 2:
        if args[1].lower() in ("todos", "all"):
            alg_ids = list(ALGORITHMS.keys())
        elif args[1].isdigit() and int(args[1]) in ALGORITHMS:
            alg_ids = [int(args[1])]
        else:
            print(f"Erro: algoritmo '{args[1]}' inválido. Escolha entre 1, 2, 3, 4 ou 'todos'.")
            sys.exit(1)
    else:
        alg_ids = list(ALGORITHMS.keys())

    return start, alg_ids, "custom"


if __name__ == "__main__":
    parsed = parse_args()

    if parsed is None:
        for case_name, state in PREDEFINED_CASES.items():
            run_case(state, case_name, list(ALGORITHMS.keys()))
    else:
        start, alg_ids, case_name = parsed
        run_case(start, case_name, alg_ids)

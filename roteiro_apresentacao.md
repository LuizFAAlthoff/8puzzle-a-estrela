# Roteiro para Apresentação em Vídeo — 8-Puzzle com A*

**Duração:** 10 minutos  
**Formato:** VSCode + Terminal (sem slides)  
**Plataforma:** YouTube

---

## 1º - Introdução e Estrutura (~ 1 min)

**Objetivo:** Apresentar o projeto e a organização dos arquivos

- Breve contexto: 8-puzzle é um clássico da IA para demonstrar buscas informadas
- Mostrar os 4 arquivos principais:
  - `puzzle.py` — Lógica do tabuleiro e validação
  - `heuristics.py` — As 4 heurísticas (Uniforme, Peças Fora, Manhattan, Não-admissível)
  - `search.py` — Implementação do algoritmo A*
  - `main.py` — Interface que roda os 7 casos padrão

---

## 2º - Funções Principais e Relação com A* (~ 1.5 min)

### **Arquivo: puzzle.py**

**Mostrar no código:**

1. **`is_solvable(state)`** (linhas 5-16)
   - Propriedade matemática: um 8-puzzle só é resolvível se tiver número **par de inversões**
   - Conta inversões na sequência linear (ignorando o espaço em branco)
   - Filtra ~50% dos estados de entrada inválidos antes de iniciar busca
   - Exemplo: Se uma configuração tiver 3 inversões (ímpar) → não tem solução

2. **`get_neighbors(state)`** (linhas 19-40)
   - Retorna os vizinhos válidos de um estado (máximo 4 movimentos: cima, baixo, esquerda, direita)
   - Valida limites da matriz 3×3
   - Retorna tuplas `(novo_estado, movimento)`
   - **Crucial no A*:** esta função é chamada dentro do loop de expansão

3. **`print_board(state)`** (linhas 43-48)
   - Apenas formatação visual (não afeta algoritmo)

---

## 3º - Gerenciamento da Fronteira no A* (~ 2 min)

### **Arquivo: search.py**

**Mostrar estrutura da fronteira (linhas 11-25):**
```
Fronteira = Lista ordenada com entradas: (f, g, counter, state)
  f       = g + h   → custo estimado total
  g       = custo real acumulado
  counter = desempate (evita comparar tuplas grandes)
  state   = tupla do tabuleiro (9 inteiros)
```

**Mostrar verificações antes de enfileirar (linhas 77-87):**

1. **Se vizinho está em `closed` → DESCARTAR**
   - Conjunto `closed` contém estados já expandidos com custo ótimo
   - Evita revisitar nodos desnecessariamente

2. **Se já existe `g_costs[vizinho] ≤ novo_g` → DESCARTAR**
   - Já temos caminho mais barato (ou igual) conhecido para este estado
   - Usa dicionário `g_costs` para rastrear custos reais
   - Só enfileira se encontrar caminho mais barato

3. **Se `vizinho` já na fronteira com custo melhor → ATUALIZAR**
   - A função `insort()` mantém a lista ordenada por `f` automaticamente
   - Garante nodos com menor f-value são expandidos primeiro (propriedade do A*)

**Mostrar rastreamento (linhas 54-55, 73):**
- `visited_count`: conta quantos nodos foram expandidos (forem do `closed`)
- `max_frontier_size`: rastreia o maior tamanho da fronteira durante execução

---

## 4º - As 4 Heurísticas (~ 3 min)

### **Arquivo: heuristics.py**

**Mostrar cada heurística no código:**

#### **1. h_zero() — Custo Uniforme**
```python
Retorna sempre 0 → A* degrada em Dijkstra (custo uniforme)
```
- Sem heurística = garante solução ótima, mas explora muitos nodos
- Baseline para comparação

#### **2. h_pecas_fora() — Admissível Simples** (linhas 36-39)
- Conta quantas peças estão fora do lugar
- **Admissível:** cada peça precisa de ≥1 movimento → nunca superestima
- Rápida de calcular (um loop)
- Menos precisa que Manhattan

#### **3. h_manhattan() — Admissível Precisa** (linhas 42-54)
```
Para cada peça: distância = |linha_atual - linha_goal| + |coluna_atual - coluna_goal|
```
- **Admissível:** ignora colisões entre peças (subestima)
- **Domina h_pecas_fora:** Manhattan(s) ≥ Peças_Fora(s) para todo estado s
- Mais precisa → menos nodos expandidos
- Exemplo: peça 8 em posição (2,0) e goal em (2,2) → distância = 2

#### **4. h_inadmissivel() — Não-Admissível (Soma)** (linhas 28-32)
```
h = h_pecas_fora(state) + h_manhattan(state)
```
- Soma duas heurísticas admissíveis → resulta em superestimação
- **NÃO admissível:** pode superestimar verdadeiro custo
- Expande menos nodos que Manhattan, mas solução pode não ser ótima
- Compara trade-off: velocidade vs. otimalidade

**Comparação visual (indicar na tela):**
```
Manhattan domina Peças_Fora domina Custo_Uniforme
```

---

## 5º - Execução e Resultados (~ 2 min)

### **Terminal: Rodar o programa**
```powershell
&"c:\Users\Luiz Fernando\8puzzle-a-estrela\.venv\Scripts\python.exe" "c:\Users\Luiz Fernando\8puzzle-a-estrela\main.py"
```

**Mostrar saída para pelo menos:**

**Caso FÁCIL (ex: FACIL_1):**
```
Algoritmo                         Visitados  Caminho    Tempo(s)   MaxFront
─────────────────────────────────────────────────────────────────────────
Custo Uniforme                           17        3    0.000104         14
A* Peças Fora do Lugar                    4        3    0.000038          6
A* Manhattan                              4        3    0.000047          6
A* Não Admissível (Soma)                  4        3    0.000062          6
```

**Análise do FÁCIL:**
- A* reduz visitados de 17 (uniforme) para 4 (heurísticas)
- Todos encontram solução ótima (tamanho = 3)
- Heurísticas dominam completamente

**Caso MÉDIO (ex: MEDIO_1):**
- Mostrar ganho ainda mais significativo
- Mencionar ordem de precisão: Manhattan ≤ Peças_Fora ≤ Uniforme em nodos visitados

**Caso DIFÍCIL (ex: DIFICIL_1):**
- Mostrar diferença ainda mais acentuada
- A* com Manhattan é essencial para viabilidade

### **Tabela Comparativa Geral (Mínimo solicitado):**
- ✅ 1 fácil (FACIL_1 ou FACIL_2)
- ✅ 1 médio (MEDIO_1 ou MEDIO_2)  
- ✅ 1 difícil (DIFICIL_1 ou DIFICIL_2)
- ✅ Todos os 4 algoritmos para cada caso

---

## 6º - Análise de Desempenho e Conclusões (~ 0.5 min)

**Destacar no vídeo:**

| Métrica | Custo Uniforme | Peças Fora | Manhattan | Não-Admissível |
|---------|---|---|---|---|
| **Admissível?** | ✅ Sim | ✅ Sim | ✅ Sim | ❌ Não |
| **Precisão** | 0 | Baixa | Alta | Alta |
| **Nodos Visitados** | Mais | Menos | Menos | Menos |
| **Otimalidade** | ✅ Ótimo | ✅ Ótimo | ✅ Ótimo | ❌ Pode não ser |
| **Uso Prático** | Não | Básico | ✅ Recomendado | Experimentos |

**Conclusão:**
- Manhattan é a melhor opção para este problema (admissível + precisa)
- A* com Manhattan é ~4-10x mais eficiente que Custo Uniforme
- Heurística não-admissível é mais rápida mas não garante otimalidade 

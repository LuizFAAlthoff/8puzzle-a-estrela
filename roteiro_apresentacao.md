# Roteiro para Apresentação em Vídeo — 8-Puzzle com A*

**Duração:** 10 minutos  
**Formato:** VSCode + Terminal (sem slides)  
**Plataforma:** YouTube

---

## 1º - Introdução e Estrutura (~ 1 min)

**Objetivo:** apresentar o projeto e situar o que foi implementado.

**O que eu posso falar:**

“Neste trabalho eu implementei a busca A* para resolver o problema do 8-puzzle. A ideia é começar com um tabuleiro embaralhado e encontrar a sequência mínima de movimentos para chegar ao estado objetivo. Esse problema é interessante porque permite comparar uma busca sem heurística, como custo uniforme, com buscas informadas usando heurísticas diferentes.”

“A organização do projeto ficou separada em quatro arquivos principais. No `puzzle.py` eu deixei a lógica do tabuleiro e a verificação de solucionabilidade. No `heuristics.py` estão as heurísticas usadas pelo A*. No `search.py` está a implementação da busca em si. E no `main.py` está a parte que executa os casos, mostra os resultados e salva os arquivos de saída.”

“Na execução padrão, o programa roda casos fáceis, médios, difíceis e um aleatório, então eu consigo comparar o comportamento dos algoritmos em diferentes níveis de dificuldade.”

---

## 2º - Funções Principais e Relação com A* (~ 1.5 min)

### **Arquivo: `puzzle.py`**

**O que eu posso falar sobre `e_resolvivel(estado)`:**

“Antes de iniciar a busca, eu verifico se o estado inicial tem solução. Para o 8-puzzle com um objetivo fixo, isso depende da quantidade de inversões. Se o número de inversões for par, o estado é resolvível; se for ímpar, não tem solução. Essa checagem evita gastar tempo tentando resolver configurações impossíveis.”

“Na prática, isso filtra uma parte grande dos estados de entrada e deixa o algoritmo mais eficiente logo no início.”

**O que eu posso falar sobre `obter_vizinhos(estado)`:**

“Essa função é uma das mais importantes da implementação, porque ela gera os próximos estados possíveis a partir do estado atual. Ela localiza o espaço em branco, calcula os movimentos válidos dentro dos limites do tabuleiro e retorna os vizinhos junto com o movimento realizado.”

“No A*, essa função é chamada toda vez que um estado é expandido. Então ela é diretamente responsável por gerar a fronteira de novos estados.”

**O que eu posso falar sobre `imprimir_tabuleiro(estado)`:**

“Essa função é só para visualização. Ela formata o tabuleiro para ficar legível no terminal, mas não interfere na lógica da busca.”

---

## 3º - Gerenciamento da Fronteira no A* (~ 2 min)

### **Arquivo: `search.py`**

**O que eu posso falar sobre a estrutura da fronteira:**

“No A*, eu mantenho a fronteira como uma lista ordenada de tuplas no formato `(f, g, contador, estado)`. O `f` é a soma do custo acumulado com a heurística, o `g` é o custo real até aquele estado, o `contador` serve para desempatar entradas com o mesmo valor de `f`, e o `estado` é o tabuleiro em si.”

“Essa estrutura permite que eu sempre expanda primeiro o estado com menor custo estimado total.”

**O que eu posso falar sobre as verificações antes de enfileirar um vizinho:**

“Antes de adicionar um vizinho na fronteira, eu faço duas verificações principais. Primeiro, se o estado já está no conjunto de fechados, eu descarto, porque ele já foi expandido com o melhor custo conhecido.”

“Depois, eu verifico se já existe um custo `g` menor ou igual registrado para esse mesmo estado. Se existir, eu também descarto, porque já há um caminho melhor ou equivalente conhecido.”

“Se o novo caminho for melhor, eu atualizo o custo, guardo o predecessor e insiro o estado de forma ordenada na fronteira.”

**O que eu posso falar sobre `inserir_ordenado()`:**

“Em vez de usar uma função pronta de biblioteca externa, eu implementei uma inserção ordenada própria com busca binária. Assim eu mantenho a lista organizada por prioridade e consigo controlar melhor a lógica do algoritmo.”

**O que eu posso falar sobre os contadores de execução:**

“Durante a busca, eu também registro quantos estados foram visitados e qual foi o maior tamanho atingido pela fronteira. Essas métricas são importantes para comparar o desempenho entre as heurísticas.”

---

## 4º - As 4 Heurísticas (~ 3 min)

### **Arquivo: `heuristics.py`**

**O que eu posso falar sobre `heuristica_nula()`:**

“Essa é a heurística usada para representar custo uniforme. Ela sempre retorna zero, então o A* vira praticamente uma busca de custo uniforme, sem nenhuma informação adicional do objetivo.”

“Ela é útil como linha de base, porque garante solução ótima, mas normalmente expande muito mais estados.”

**O que eu posso falar sobre `heuristica_pecas_fora_lugar()`:**

“Essa heurística conta quantas peças estão fora da posição correta. Ela é admissível porque cada peça fora do lugar precisa de pelo menos um movimento para chegar à posição certa, então ela nunca superestima o custo real.”

“Ela é simples e rápida de calcular, mas menos precisa do que a Manhattan.”

**O que eu posso falar sobre `heuristica_manhattan()`:**

“A heurística Manhattan soma, para cada peça, a distância horizontal e vertical até a posição objetivo. Em outras palavras, ela calcula quantos passos cada peça ainda precisa percorrer, ignorando colisões com outras peças.”

“Ela também é admissível, porque tende a subestimar o custo real. Entre as heurísticas admissíveis que eu implementei, ela é a mais precisa, então costuma expandir menos estados.”

“Se eu quiser dar um exemplo rápido, a peça 8, por exemplo, se estiver em uma posição distante duas colunas do objetivo, a distância Manhattan dela é 2.”

**O que eu posso falar sobre `heuristica_inadmissivel()`:**

“Essa heurística soma a quantidade de peças fora do lugar com a distância Manhattan. Como estou combinando duas estimativas, ela pode superestimar o custo real, então ela não é admissível.”

“A vantagem é que ela pode reduzir ainda mais a quantidade de estados visitados, mas em troca perde a garantia de otimalidade da solução.”

**Fechamento dessa parte:**

“Na comparação geral, a Manhattan é mais informativa do que peças fora do lugar, e as duas são melhores do que custo uniforme em termos de eficiência.”

---

## 5º - Execução e Resultados (~ 2 min)

### **Terminal: rodar o programa**

“Agora eu vou executar o programa para mostrar os resultados práticos.”

```powershell
&"c:\Users\Luiz Fernando\8puzzle-a-estrela\.venv\Scripts\python.exe" "c:\Users\Luiz Fernando\8puzzle-a-estrela\main.py"
```

**O que eu posso falar ao mostrar o caso fácil:**

“No caso fácil, dá para ver que todas as buscas encontram a mesma solução, mas o custo uniforme visita muito mais estados. Já as versões com heurística chegam à solução com bem menos expansões.”

“Isso mostra que a heurística realmente orienta melhor a busca.”

**O que eu posso falar ao mostrar o caso médio:**

“No caso médio, a diferença fica mais clara. A Manhattan costuma visitar menos nós do que peças fora do lugar, porque ela fornece uma estimativa mais precisa da distância até o objetivo.”

“Aqui também dá para ver melhor a relação entre precisão da heurística e eficiência da busca.”

**O que eu posso falar ao mostrar o caso difícil:**

“No caso difícil, a vantagem da busca informada fica ainda mais evidente. Se eu usasse só custo uniforme, a quantidade de estados explorados seria muito maior. Com a heurística Manhattan, a busca continua viável.”

**Como eu posso resumir a tabela comparativa:**

“A tabela comparativa junta os números de estados visitados, tamanho do caminho, tempo de execução e maior fronteira. Com isso eu consigo mostrar o impacto das heurísticas de forma objetiva.”

“A ideia principal é que, para o 8-puzzle, uma heurística mais precisa normalmente reduz bastante o custo de busca.”

---

## 6º - Análise de Desempenho e Conclusões (~ 0.5 min)

**O que eu posso falar no fechamento:**

“Com base nos testes, a heurística Manhattan foi a melhor opção entre as admissíveis, porque consegue equilibrar otimalidade e eficiência. A heurística de peças fora do lugar também funciona bem, mas é menos informativa.”

“O custo uniforme garante solução ótima, mas é o menos eficiente. Já a heurística não admissível pode ser ainda mais agressiva na redução de estados, mas sem garantir que a solução encontrada seja a menor possível.”

“Então, no meu trabalho, a conclusão é que o A* com Manhattan foi a abordagem mais adequada para resolver o 8-puzzle de forma correta e eficiente.”

**Se quiser encerrar com uma frase curta:**

“Em resumo, o trabalho mostra bem a diferença entre busca sem heurística e busca informada, e como a escolha da heurística afeta diretamente o desempenho do algoritmo.”

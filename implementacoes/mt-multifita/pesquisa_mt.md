# Pesquisa Conceitual — Máquina de Turing com Múltiplas Fitas
**AV2 — Teoria da Computabilidade — CESUPA 01/2026**

---

## 1. Contextualização histórica

A Máquina de Turing foi proposta por Alan Turing em 1936 no artigo *"On Computable Numbers, with an Application to the Entscheidungsproblem"*, como um modelo matemático para formalizar a noção de algoritmo e demonstrar que certos problemas são indecidíveis. O modelo original consistia em uma única fita infinita, uma cabeça de leitura/escrita e um conjunto finito de estados.

A variante com múltiplas fitas surgiu naturalmente como extensão para facilitar a descrição de algoritmos complexos. Autores como John Hopcroft e Jeffrey Ullman consolidaram o modelo multifita na literatura ao demonstrar formalmente, nas décadas de 1960 e 1970, que toda MT com k fitas pode ser simulada por uma MT de fita única — estabelecendo assim a equivalência computacional entre os modelos, ainda que com diferença de eficiência.

---

## 2. Definição formal

Uma Máquina de Turing com k fitas é definida pela 7-upla:

```
M = (Q, Σ, Γ, δ, q₀, q_aceita, q_rejeita)
```

onde:

| Componente | Descrição |
|------------|-----------|
| Q | Conjunto finito de estados |
| Σ | Alfabeto de entrada (não contém o branco B) |
| Γ | Alfabeto de fita, com Σ ⊆ Γ e B ∈ Γ |
| δ | Função de transição: Q × Γᵏ → Q × Γᵏ × {L, R, S}ᵏ |
| q₀ ∈ Q | Estado inicial |
| q_aceita ∈ Q | Estado de aceitação |
| q_rejeita ∈ Q | Estado de rejeição (q_rejeita ≠ q_aceita) |

A função de transição δ recebe o estado atual e os símbolos lidos pelas k cabeças, e produz o próximo estado, os símbolos a escrever em cada fita e a direção de cada cabeça (L = esquerda, R = direita, S = estacionário).

### Configuração

Uma configuração da MT multifita é uma tupla:

```
(q, w₁, p₁, w₂, p₂, ..., wₖ, pₖ)
```

onde q é o estado atual, wᵢ é o conteúdo da fita i e pᵢ é a posição da cabeça na fita i.

### Critério de aceitação

A máquina aceita uma entrada w se, partindo da configuração inicial (q₀, w, 0, B, 0, ..., B, 0), existe uma sequência de passos que leva ao estado q_aceita. Rejeita se atinge q_rejeita ou se não há transição definida.

---

## 3. Nosso modelo — implementação específica

### Parâmetros da máquina implementada

```
M = (Q, Σ, Γ, δ, q0, q_aceita, q_rejeita)

Q  = {q0, q1, q2, q3, q4, q5, q6, q7, q8, q_aceita, q_rejeita}  — 11 estados
Σ  = {a, b}
Γ  = {a, b, B}
k  = 2 fitas
q₀ = q0
```

### Função de transição (tabela resumida)

| Estado | Lê F1 | Lê F2 | Escreve F1 | Dir F1 | Escreve F2 | Dir F2 | Próx. estado |
|--------|--------|--------|------------|--------|------------|--------|--------------|
| q0 | a | B | a | R | a | L | q0 |
| q0 | b | B | b | R | b | L | q0 |
| q0 | B | B | B | S | B | R | q1 |
| q1 | B | a | B | R | a | S | q3 |
| q1 | B | b | B | R | b | S | q3 |
| q2 | a | B | a | L | B | S | q2 |
| q2 | b | B | b | L | B | S | q2 |
| q2 | B | B | B | R | B | S | q3 |
| q3 | a | a | a | R | a | R | q4 |
| q3 | b | b | b | R | b | R | q4 |
| q3 | B | B | B | S | B | S | q_aceita |
| q3 | a | b | a | S | b | S | q_rejeita |
| q3 | b | a | b | S | a | S | q_rejeita |
| q4 | a | a | a | R | a | R | q4 |
| q4 | b | b | b | R | b | R | q4 |
| q4 | B | B | B | S | B | S | q_aceita |
| q4 | a | b | a | S | b | S | q_rejeita |
| q4 | b | a | b | S | a | S | q_rejeita |

---

## 4. Relação com a Hipótese de Church-Turing

A Hipótese de Church-Turing afirma que qualquer função efetivamente computável pode ser computada por uma Máquina de Turing. A MT multifita não amplia a classe das funções computáveis — ela computa exatamente a mesma classe que a MT de fita única. O que muda é a eficiência:

- Uma MT de fita única que resolve palíndromo em cadeias de comprimento n pode precisar de O(n²) passos (pela necessidade de varrer a fita ida e volta múltiplas vezes).
- A MT de 2 fitas resolve o mesmo problema em O(n) passos: uma passagem para copiar, uma passagem para comparar.

Formalmente, o Teorema da Equivalência das Múltiplas Fitas (Sipser, 2012, Theorem 3.13) garante:

> Toda Máquina de Turing com k fitas tem uma Máquina de Turing equivalente de fita única. Se a MT multifita decide uma linguagem em tempo t(n), a MT de fita única equivalente a decide em tempo O(t(n)²).

---

## 5. Relação com classes de linguagens

A MT multifita, como a MT padrão, reconhece exatamente as **linguagens recursivamente enumeráveis** (RE). As linguagens **decidíveis** (recursivas) são aquelas para as quais a MT sempre para — seja aceitando ou rejeitando. Nossa implementação é um decisor: para toda entrada sobre {a, b}, a máquina sempre para.

A linguagem dos palíndromos sobre {a, b} é:
- Livre de contexto (pode ser gerada por uma gramática livre de contexto)
- Decidível (nossa MT decide em O(n))
- Não regular (nenhum AFD pode reconhecê-la — pelo Lema do Bombeamento)

---

## 6. Comparação: MT de fita única vs. MT multifita

| Aspecto | MT fita única | MT 2 fitas (nossa) |
|---------|--------------|---------------------|
| Poder computacional | Igual | Igual |
| Complexidade de tempo para palíndromo | O(n²) | O(n) |
| Complexidade de espaço | O(n) | O(n) |
| Facilidade de programação | Maior dificuldade | Mais natural |
| Número de estados para palíndromo | Muito maior | 11 estados |

---

## 7. Limitações observadas

- O modelo implementado não aceita a cadeia vazia — seria necessário adicionar uma transição de q0 para q_aceita ao ler branco antes de qualquer símbolo, caso se queira considerar ε como palíndromo.
- A máquina só aceita o alfabeto {a, b}. Extensão para alfabetos maiores exige duplicar as transições de cópia e comparação para cada novo símbolo.
- O arquivo JFLAP da MT multifita pode apresentar variações de comportamento dependendo da versão do JFLAP utilizada, pois o suporte a múltiplas fitas foi introduzido em versões mais recentes.

---

## 8. Referências

- TURING, Alan M. On Computable Numbers, with an Application to the Entscheidungsproblem. *Proceedings of the London Mathematical Society*, v. 42, p. 230–265, 1936.
- DIVERIO, Tiarajú A.; MENEZES, Paulo B. **Teoria da Computação: Máquinas Universais e Computabilidade.** 3. ed. Porto Alegre: Bookman, 2011. cap. 5.
- SIPSER, Michael. **Introduction to the Theory of Computation.** 3. ed. Boston: Cengage, 2012. Theorem 3.13, p. 176–178.
- HOPCROFT, John E.; ULLMAN, Jeffrey D. **Introduction to Automata Theory, Languages, and Computation.** Reading: Addison-Wesley, 1979.
- Slides da disciplina — Prof. Daniel Leal Souza, CESUPA, 01/2026.

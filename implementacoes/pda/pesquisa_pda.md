# Pesquisa Conceitual — Autômato de Pilha (PDA)
**AV2 — Teoria da Computabilidade — CESUPA 01/2026**

---

## 1. Contextualização histórica

O Autômato de Pilha (do inglês *Pushdown Automaton*, PDA) surgiu como extensão dos Autômatos Finitos para lidar com linguagens que exigem memória ilimitada de contagem ou balanceamento. O modelo foi formalizado por Noam Chomsky e outros pesquisadores no final da década de 1950 e início da de 1960, em paralelo ao desenvolvimento da Hierarquia de Chomsky.

O trabalho de Chomsky (1956, 1959) estabeleceu a correspondência entre gramáticas livres de contexto (Tipo 2 da hierarquia) e autômatos de pilha — resultado que se tornaria um dos pilares da teoria das linguagens formais. Posteriormente, Schützenberger (1963) formalizou os PDAs determinísticos, que reconhecem uma subclasse estrita das linguagens livres de contexto.

O modelo ganhou enorme relevância prática: compiladores utilizam PDAs (ou variantes equivalentes como parsers LL e LR) para análise sintática de linguagens de programação, tornando o PDA um dos modelos teóricos com maior impacto direto na engenharia de software.

---

## 2. Definição formal

Um Autômato de Pilha é definido pela 7-upla:

```
M = (Q, Σ, Γ, δ, q₀, Z₀, F)
```

onde:

| Componente | Descrição |
|------------|-----------|
| Q | Conjunto finito de estados |
| Σ | Alfabeto de entrada |
| Γ | Alfabeto de pilha |
| δ | Função de transição: Q × (Σ ∪ {ε}) × Γ → P(Q × Γ*) |
| q₀ ∈ Q | Estado inicial |
| Z₀ ∈ Γ | Símbolo inicial da pilha (marcador de fundo) |
| F ⊆ Q | Conjunto de estados de aceitação |

A função de transição δ(q, a, X) retorna um conjunto de pares (p, γ), onde p é o próximo estado e γ é a cadeia que substitui o topo X da pilha. Quando a = ε, ocorre uma transição espontânea (sem consumir símbolo da entrada).

### Configuração

Uma configuração do PDA é uma tripla (q, w, α), onde:
- q ∈ Q é o estado atual
- w ∈ Σ* é o restante da entrada a ser consumido
- α ∈ Γ* é o conteúdo atual da pilha (topo à esquerda)

### Critério de aceitação

Existem dois critérios equivalentes:

1. **Por estado final:** A entrada w é aceita se existe uma sequência de movimentos de (q₀, w, Z₀) até (q_f, ε, α), com q_f ∈ F (qualquer conteúdo de pilha).
2. **Por pilha vazia:** A entrada w é aceita se existe uma sequência que leva a (q, ε, ε) para algum estado q.

Nossa implementação usa aceitação por estado final com verificação de Z₀ no topo.

---

## 3. Nosso modelo — implementação específica

### Parâmetros da máquina implementada

```
M = (Q, Σ, Γ, δ, q0, Z0, F)

Q  = {q0, q1, q2, q3, q4, q5, q6, q7, q8, q_aceita, q_rejeita}  — 11 estados
Σ  = {a, b}
Γ  = {A, Z0}
q₀ = q0
Z₀ = Z0
F  = {q_aceita}
```

### Função de transição (tabela completa)

| Estado | Lê entrada | Topo da pilha | Próx. estado | Ação na pilha |
|--------|-----------|---------------|--------------|---------------|
| q0 | a | Z0 | q1 | empilha A (pilha: AZ0) |
| q0 | b | Z0 | q_rejeita | noop |
| q1 | a | A | q2 | empilha A (pilha: AAZ0) |
| q1 | b | A | q3 | desempilha A |
| q2 | a | A | q5 | empilha A (pilha: AAAZ0) |
| q2 | b | A | q4 | desempilha A |
| q3 | ε | Z0 | q_aceita | noop |
| q3 | a | A | q_rejeita | noop |
| q3 | b | A | q_rejeita | noop |
| q3 | a | Z0 | q_rejeita | noop |
| q3 | b | Z0 | q_rejeita | noop |
| q4 | b | A | q8 | desempilha A |
| q4 | ε | Z0 | q_rejeita | noop |
| q4 | a | A | q_rejeita | noop |
| q4 | a | Z0 | q_rejeita | noop |
| q4 | b | Z0 | q_rejeita | noop |
| q5 | a | A | q6 | empilha A (pilha: AAAAZ0) |
| q5 | b | A | q7 | desempilha A |
| q5 | a | Z0 | q_rejeita | noop |
| q5 | b | Z0 | q_rejeita | noop |
| q6 | a | A | q6 | empilha A (loop) |
| q6 | b | A | q7 | desempilha A |
| q6 | a | Z0 | q_rejeita | noop |
| q6 | b | Z0 | q_rejeita | noop |
| q7 | b | A | q8 | desempilha A |
| q7 | a | A | q_rejeita | noop |
| q7 | a | Z0 | q_rejeita | noop |
| q7 | b | Z0 | q_rejeita | noop |
| q7 | ε | A | q_rejeita | noop |
| q8 | b | A | q8 | desempilha A (loop) |
| q8 | ε | Z0 | q_aceita | noop |
| q8 | a | A | q_rejeita | noop |
| q8 | a | Z0 | q_rejeita | noop |
| q8 | b | Z0 | q_rejeita | noop |

### Exemplo de computação para `aabb`

```
Configuração inicial: (q0, aabb, Z0)

Passo 1: δ(q0, a, Z0) = (q1, AZ0)   → (q1, abb, AZ0)
Passo 2: δ(q1, a, A)  = (q2, AAZ0)  → (q2, bb, AAZ0)
Passo 3: δ(q2, b, A)  = (q4, AZ0)   → (q4, b, AZ0)
Passo 4: δ(q4, b, A)  = (q8, Z0)    → (q8, ε, Z0)
Passo 5: δ(q8, ε, Z0) = (q_aceita, Z0) → ACEITA
```

---

## 4. Relação com a Hipótese de Church-Turing e computabilidade

O PDA reconhece exatamente as **Linguagens Livres de Contexto (LLC)** — Tipo 2 da Hierarquia de Chomsky. Isso o posiciona abaixo da Máquina de Turing em poder computacional:

```
Linguagens Regulares ⊊ Linguagens Livres de Contexto ⊊ Linguagens Decidíveis ⊊ Linguagens RE
       AFD/AFN               PDA / GLC                    MT (decisor)             MT geral
```

A linguagem L = {aⁿbⁿ | n ≥ 1} é livre de contexto mas não regular. A prova de que não é regular utiliza o Lema do Bombeamento para linguagens regulares: para qualquer constante p, a cadeia aᵖbᵖ não pode ser bombeada sem sair da linguagem.

A Hipótese de Church-Turing estabelece que o PDA, apesar de computacionalmente mais fraco que a MT, ainda formaliza um modelo de computação preciso e rigoroso — adequado para a classe de problemas que podem ser resolvidos com uma pilha como única memória auxiliar.

---

## 5. PDA determinístico vs. não determinístico

| Aspecto | PDA Determinístico (DPDA) | PDA Não Determinístico (NPDA) |
|---------|--------------------------|-------------------------------|
| Transições | δ retorna no máximo 1 par | δ retorna um conjunto de pares |
| Poder | Reconhece subclasse das LLC | Reconhece todas as LLC |
| Equivalência com MT | Não equivalente | Não equivalente |
| Exemplo | aⁿbⁿ (nossa impl.) | Palíndromos sobre {a,b}* |

A linguagem L = {aⁿbⁿ} é reconhecida por um DPDA (nossa implementação). Já a linguagem dos palíndromos sobre {a, b}* exige um NPDA — não existe DPDA que a reconheça, pois o autômato precisa "adivinhar" o meio da cadeia.

Essa distinção é relevante: DPDA ⊊ LLC, ou seja, PDAs determinísticos reconhecem estritamente menos linguagens que PDAs não determinísticos — diferentemente do que ocorre com autômatos finitos (AFD = AFN em poder).

---

## 6. Relação com gramáticas livres de contexto

Pelo Teorema de Equivalência (Sipser, 2012, Theorem 2.20):

> Uma linguagem é livre de contexto se e somente se algum autômato de pilha a reconhece.

A gramática que gera L = {aⁿbⁿ | n ≥ 1} é:

```
S → aSb | ab
```

O PDA implementado é a contraparte operacional desta gramática: cada 'a' lido corresponde a um passo de derivação S → aSb, e cada 'b' lido à conclusão com 'ab'.

---

## 7. Comparação: PDA vs. Autômato Finito vs. MT

| Aspecto | AFD | PDA (nossa impl.) | MT |
|---------|-----|-------------------|----|
| Memória auxiliar | Nenhuma | Pilha (LIFO) | Fita infinita |
| Classe reconhecida | Regulares | LLC | RE |
| aⁿbⁿ | Não reconhece | Reconhece | Reconhece |
| aⁿbⁿcⁿ | Não reconhece | Não reconhece | Reconhece |
| Decisão sempre para? | Sim | Sim (DPDA) | Nem sempre |

---

## 8. Limitações observadas

- O PDA implementado é determinístico e aceita exatamente {aⁿbⁿ | n ≥ 1}. Para n = 0 (cadeia vazia), a máquina rejeita — caso se queira incluir ε, é necessário adicionar uma transição inicial.
- A pilha implementa apenas contagem de igualdade entre a's e b's. Para reconhecer {aⁿbⁿcⁿ}, seria necessária uma MT (ou dois contadores), pois o PDA não consegue verificar três quantidades simultaneamente com uma pilha.
- O não determinismo dos PDAs em geral não pode ser eliminado para todas as LLCs — isso diferencia os PDAs dos autômatos finitos e é uma fonte de complexidade na implementação de parsers reais.

---

## 9. Referências

- CHOMSKY, Noam. Three Models for the Description of Language. *IRE Transactions on Information Theory*, v. 2, n. 3, p. 113–124, 1956.
- CHOMSKY, Noam. On Certain Formal Properties of Grammars. *Information and Control*, v. 2, p. 137–167, 1959.
- DIVERIO, Tiarajú A.; MENEZES, Paulo B. **Teoria da Computação: Máquinas Universais e Computabilidade.** 3. ed. Porto Alegre: Bookman, 2011. cap. 3–4.
- MENEZES, Paulo B. **Linguagens Formais e Autômatos.** 6. ed. Porto Alegre: Bookman, 2011. cap. 5.
- SIPSER, Michael. **Introduction to the Theory of Computation.** 3. ed. Boston: Cengage, 2012. Theorem 2.20, p. 115–116.
- HOPCROFT, John E.; MOTWANI, Rajeev; ULLMAN, Jeffrey D. **Introduction to Automata Theory, Languages, and Computation.** 3. ed. Pearson, 2006. cap. 6.
- Slides da disciplina — Prof. Daniel Leal Souza, CESUPA, 01/2026.

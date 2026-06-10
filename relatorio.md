# Relatório do Trabalho — AV2 Teoria da Computabilidade

## 1. Identificação

- Disciplina: Teoria da Computabilidade
- Professor: Daniel Leal Souza
- Semestre: 01/2026
- Alunos: Pedro Lyra, VIthor dos Santos, Murilo Carneiro, João Felipe Soares

---

## 2. Objetivo

O trabalho desenvolve e documenta dois modelos formais:

1. Máquina de Turing com Múltiplas Fitas (Opção 3) para reconhecer palíndromos sobre o alfabeto `{a, b}`.
2. Autômato de Pilha (PDA) para reconhecer a linguagem `L = {aⁿbⁿ | n ≥ 1}`.

O relatório apresenta o modelo implementado para a MT multifita, a lógica de execução, os testes, a análise de complexidade e as conclusões sobre o projeto.

---

## 3. Máquina de Turing com Múltiplas Fitas

### 3.1 Contexto

A Máquina de Turing foi proposta por Alan Turing em 1936 como modelo matemático de computação. A variante com múltiplas fitas mantém o mesmo poder computacional da MT de fita única, mas permite uma descrição mais direta e eficiente de algoritmos que exigem cópia ou comparação simultânea de dados.

### 3.2 Definição formal

A MT multifita é definida por:

```
M = (Q, Σ, Γ, δ, q₀, q_aceita, q_rejeita)
```

Onde:

- `Q` é o conjunto finito de estados.
- `Σ` é o alfabeto de entrada.
- `Γ` é o alfabeto de fita, com `Σ ⊆ Γ` e `B ∈ Γ`.
- `δ` é a função de transição: `Q × Γᵏ → Q × Γᵏ × {L, R, S}ᵏ`.
- `q₀` é o estado inicial.
- `q_aceita` é o estado de aceitação.
- `q_rejeita` é o estado de rejeição.

### 3.3 Parâmetros da implementação

Para a máquina implementada:

- `Q = {q0, q1, q2, q3, q4, q5, q6, q7, q8, q_aceita, q_rejeita}` — 11 estados no conjunto formal
- `Σ = {a, b}`
- `Γ = {a, b, B}`
- `k = 2` fitas
- `q₀ = q0`
- `q_aceita` e `q_rejeita` são estados finais

Na implementação em Python, o comportamento ativo usa os estados `q0`, `q1`, `q2`, `q3`, `q4`, `q_aceita` e `q_rejeita` para realizar a cópia e comparação.

### 3.4 Estratégia de operação

A máquina resolve palíndromos em três fases:

1. **Cópia reversa** (`q0`): copia a entrada de `Fita 1` para `Fita 2` em ordem inversa. `Fita 1` avança para a direita enquanto `Fita 2` avança para a esquerda.
2. **Reposicionamento** (`q1`, `q2`): detecta o fim da entrada em `Fita 1` e reposiciona as cabeças para iniciar a comparação.
3. **Comparação** (`q3`, `q4`): lê as duas fitas simultaneamente, avançando ambas para a direita. Se todos os pares de símbolos coincidirem até o branco, a máquina aceita.

A aceitação ocorre quando ambas as fitas leem o símbolo branco `B` ao mesmo tempo. Rejeição ocorre se aparecem símbolos diferentes ou se o término das fitas é assimétrico.

### 3.5 Tabela de transição resumida

| Estado | Lê F1 | Lê F2 | Escreve F1 | Dir F1 | Escreve F2 | Dir F2 | Próximo estado |
|--------|-------|-------|------------|--------|------------|--------|----------------|
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

## 4. Implementação e demonstração

O simulador em Python está em:

- `implementacoes/mt-multifita/simulador_mt.py`

Ele roda em Python 3.8+ e não exige dependências externas.

### Comando de execução

```powershell
python implementacoes\mt-multifita\simulador_mt.py --testes
```

### Resultado observado

- `7/7 testes passaram`
- O simulador imprime, passo a passo:
  - estado atual
  - símbolo lido em `Fita 1` e `Fita 2`
  - ação de escrita
  - movimento das cabeças
  - decisão final

---

## 5. Testes realizados

Foram testadas as seguintes entradas:

- `aba` → ACEITA
- `abba` → ACEITA
- `aabaa` → ACEITA
- `a` → ACEITA
- `ab` → REJEITA
- `aab` → REJEITA
- `abab` → REJEITA

Esses testes confirmam que a máquina reconhece corretamente palíndromos e rejeita cadeias não palíndromas.

---

## 6. Análise de complexidade

A MT multifita faz duas passagens principais:

- cópia da entrada em ordem inversa;
- comparação de símbolos na direção direita.

Assim, a complexidade temporal observada é `O(n)`.

---

## 7. Observações sobre o trabalho

- A implementação aceita apenas o alfabeto `{a, b}`.
- A cadeia vazia `ε` não está contemplada na versão atual.
- O uso de duas fitas torna a descrição mais direta do problema do palíndromo, comparado com a simulação em fita única.

---

## 8. Conclusão

O trabalho mostra uma Máquina de Turing de 2 fitas que decide a linguagem dos palíndromos sobre `{a, b}`. O simulador Python comprova o funcionamento com casos de aceitação e rejeição, demonstrando a vantagem da MT multifita em termos de legibilidade e eficiência para este problema.

---

## 9. Referências

- DIVERIO, Tiarajú A.; MENEZES, Paulo B. **Teoria da Computação: Máquinas Universais e Computabilidade.** 3. ed. Porto Alegre: Bookman, 2011.
- SIPSER, Michael. **Introduction to the Theory of Computation.** 3. ed. Cengage, 2012.
- Slides da disciplina — Prof. Daniel Leal Souza, CESUPA, 01/2026.

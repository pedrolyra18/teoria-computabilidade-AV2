# Rastreamento de Execução — Autômato de Pilha (PDA)
**Problema:** Reconhecedor de L = {aⁿbⁿ | n ≥ 1}  
**Modelo:** Autômato de Pilha Determinístico (Opção 9)

---

## Descrição das fases

| Fase | Estados | Descrição |
|------|---------|-----------|
| Empilhamento | q0, q1, q2, q5, q6 | Lê 'a's e empilha A, com os primeiros símbolos desenrolados em estados distintos |
| Transição | q1/q2/q5/q6 → q3/q4/q7 | Ao ler o 1º 'b', entra no ramo correto conforme o número de 'a's lidos |
| Desempilhamento | q7, q8 | Continua desempilhando um A por 'b' até a pilha voltar a Z0 |
| Decisão | q_aceita / q_rejeita | Aceita se pilha = [Z0] ao fim |

**Legenda da pilha:** Z0 = fundo, A = símbolo empilhado  
Pilha mostrada como [topo → fundo]: `[A, A, Z0]` = dois A's sobre Z0

---

## Teste 1 — Entrada: `ab` → ACEITA ✓

**Justificativa:** n=1, um 'a' e um 'b'.

| Passo | Estado | Lido | Topo | Pilha após | → Estado | Ação |
|-------|--------|------|------|------------|----------|------|
| 0 | q0 | a | Z0 | [A, Z0] | q1 | Empilha A |
| 1 | q1 | b | A | [Z0] | q4 | Desempilha A |
| 2 | q4 | ε | Z0 | [Z0] | **q_aceita** | Fim da entrada, pilha = Z0 ✓ |

**Resultado: ACEITA** — `ab` ∈ L com n=1.

---

## Teste 2 — Entrada: `aabb` → ACEITA ✓

**Justificativa:** n=2, dois 'a's seguidos de dois 'b's.

| Passo | Estado | Lido | Topo | Pilha após | → Estado | Ação |
|-------|--------|------|------|------------|----------|------|
| 0 | q0 | a | Z0 | [A, Z0] | q1 | Empilha A |
| 1 | q1 | a | A | [A, A, Z0] | q2 | Empilha A |
| 2 | q2 | b | A | [A, Z0] | q4 | Desempilha A |
| 3 | q4 | b | A | [Z0] | q8 | Desempilha A |
| 4 | q8 | ε | Z0 | [Z0] | **q_aceita** | Pilha = Z0 ✓ |

**Resultado: ACEITA** — `aabb` ∈ L com n=2.

---

## Teste 3 — Entrada: `aaabbb` → ACEITA ✓

**Justificativa:** n=3, três 'a's seguidos de três 'b's.

| Passo | Estado | Lido | Topo | Pilha após | → Estado | Ação |
|-------|--------|------|------|------------|----------|------|
| 0 | q0 | a | Z0 | [A, Z0] | q1 | Empilha A |
| 1 | q1 | a | A | [A, A, Z0] | q2 | Empilha A |
| 2 | q2 | a | A | [A, A, A, Z0] | q5 | Empilha A |
| 3 | q5 | b | A | [A, A, Z0] | q7 | Desempilha A |
| 4 | q7 | b | A | [A, Z0] | q8 | Desempilha A |
| 5 | q8 | b | A | [Z0] | q8 | Desempilha A (loop) |
| 6 | q8 | ε | Z0 | [Z0] | **q_aceita** | Pilha = Z0 ✓ |

**Resultado: ACEITA** — `aaabbb` ∈ L com n=3.

---

## Teste 4 — Entrada: `aab` → REJEITA ✗

**Justificativa:** dois 'a's mas apenas um 'b'; pilha terá um A restante.

| Passo | Estado | Lido | Topo | Pilha após | → Estado | Ação |
|-------|--------|------|------|------------|----------|------|
| 0 | q0 | a | Z0 | [A, Z0] | q1 | Empilha A |
| 1 | q1 | a | A | [A, A, Z0] | q2 | Empilha A |
| 2 | q2 | b | A | [A, Z0] | q4 | Desempilha A |
| 3 | q4 | ε | A | [A, Z0] | **q_rejeita** | Pilha ≠ Z0 — faltou um b ✗ |

**Resultado: REJEITA** — `aab` ∉ L (mais a's que b's).

---

## Teste 5 — Entrada: `abb` → REJEITA ✗

**Justificativa:** um 'a' mas dois 'b's; tentará desempilhar do Z0.

| Passo | Estado | Lido | Topo | Pilha após | → Estado | Ação |
|-------|--------|------|------|------------|----------|------|
| 0 | q0 | a | Z0 | [A, Z0] | q1 | Empilha A |
| 1 | q1 | b | A | [Z0] | q3 | Desempilha A |
| 2 | q3 | b | Z0 | [Z0] | **q_rejeita** | Sem transição para b com Z0 ✗ |

**Resultado: REJEITA** — `abb` ∉ L (mais b's que a's).

---

## Teste 6 — Entrada: `ba` → REJEITA ✗

**Justificativa:** começa com 'b' sem nenhum 'a' empilhado.

| Passo | Estado | Lido | Topo | Pilha após | → Estado | Ação |
|-------|--------|------|------|------------|----------|------|
| 0 | q0 | b | Z0 | [Z0] | **q_rejeita** | Sem transição para b em q0 com Z0 ✗ |

**Resultado: REJEITA** — `ba` ∉ L (ordem incorreta).

---

## Análise técnica

**Por que este exemplo não é trivial?**

A linguagem L = {aⁿbⁿ | n ≥ 1} é **não regular** — isso significa que nenhum Autômato Finito Determinístico (AFD) pode reconhecê-la. O motivo é o Lema do Bombeamento para linguagens regulares: para qualquer constante de bombeamento p, a cadeia `aᵖbᵖ` não pode ser bombeada sem sair da linguagem.

O PDA resolve isso com a pilha, que age como **memória ilimitada de contagem**: empilha um A para cada 'a' e desempilha um A para cada 'b'. A pilha implementa exatamente o que a memória finita de um AFD não consegue fazer.

**Relação com computabilidade:**
- L pertence à classe das **Linguagens Livres de Contexto (LLC)**
- PDAs reconhecem exatamente as LLCs (Teorema de Chomsky-Schützenberger)
- Toda LLC é decidível por uma MT, mas nem toda LLC é regular
- O PDA aqui é determinístico (DPDA), subclasse dos PDAs não determinísticos

**Limitações observadas:**
- O PDA não reconhece linguagens como {aⁿbⁿcⁿ | n ≥ 1}, que exigiria duas pilhas ou uma MT
- A pilha permite contar apenas uma relação de igualdade; para múltiplas relações simultâneas, o modelo é insuficiente
- O PDA determinístico implementado rejeita corretamente casos de fronteira (n=0, ordem invertida)

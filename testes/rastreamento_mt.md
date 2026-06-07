# Rastreamento de Execução — MT com Múltiplas Fitas
**Problema:** Reconhecedor de palíndromo sobre Σ = {a, b}  
**Modelo:** Máquina de Turing com 2 Fitas (Opção 3)

---

## Descrição das fases

| Fase | Estados | Descrição |
|------|---------|-----------|
| Cópia reversa | q0 | Fita 1 lê da esquerda; Fita 2 recebe a cópia invertida |
| Retorno | q1, q2 | Cabeça de Fita 1 volta ao início |
| Comparação | q3, q4 | Fita 1 e Fita 2 lidas simultaneamente |
| Decisão | q_aceita / q_rejeita | Aceita se todas as posições coincidirem |

---

## Teste 1 — Entrada: `aba` → ACEITA ✓

**Justificativa:** `aba` = reverso de `aba`, portanto é palíndromo.

| Passo | Estado | Fita 1 (cabeça) | Fita 2 (cabeça) | Ação realizada |
|-------|--------|-----------------|-----------------|----------------|
| 0 | q0 | **[a]**ba | [B] | Lê 'a' em F1, escreve 'a' em F2; F1→R, F2→L |
| 1 | q0 | a**[b]**a | **[a]** | Lê 'b' em F1, escreve 'b' em F2; F1→R, F2→L |
| 2 | q0 | ab**[a]** | **[b]**a | Lê 'a' em F1, escreve 'a' em F2; F1→R, F2→L |
| 3 | q1 | aba**[B]** | **[a]**ba | Leu branco em F1 → fim da entrada. Avança F2 |
| 4 | q3 | **[a]**ba | **[a]**ba | Inicia comparação. F1[0]=a, F2[0]=a ✓ |
| 5 | q4 | a**[b]**a | a**[b]**a | F1[1]=b, F2[1]=b ✓ |
| 6 | q4 | ab**[a]** | ab**[a]** | F1[2]=a, F2[2]=a ✓ |
| 7 | q4 | aba**[B]** | aba**[B]** | Ambas leram branco → **ACEITA** |
| 8 | **q_aceita** | — | — | ✓ |

**Resultado: ACEITA** — `aba` é palíndromo.

---

## Teste 2 — Entrada: `abba` → ACEITA ✓

**Justificativa:** `abba` = reverso de `abba`, portanto é palíndromo.

| Passo | Estado | Fita 1 (cabeça) | Fita 2 (cabeça) | Ação realizada |
|-------|--------|-----------------|-----------------|----------------|
| 0 | q0 | **[a]**bba | [B] | Copia 'a'; F1→R, F2→L |
| 1 | q0 | a**[b]**ba | **[a]** | Copia 'b'; F1→R, F2→L |
| 2 | q0 | ab**[b]**a | **[b]**a | Copia 'b'; F1→R, F2→L |
| 3 | q0 | abb**[a]** | **[b]**ba | Copia 'a'; F1→R, F2→L |
| 4 | q1 | abba**[B]** | **[a]**bba | Leu branco → avança F2 |
| 5 | q3 | **[a]**bba | **[a]**bba | F1[0]=a, F2[0]=a ✓ |
| 6 | q4 | a**[b]**ba | a**[b]**ba | F1[1]=b, F2[1]=b ✓ |
| 7 | q4 | ab**[b]**a | ab**[b]**a | F1[2]=b, F2[2]=b ✓ |
| 8 | q4 | abb**[a]** | abb**[a]** | F1[3]=a, F2[3]=a ✓ |
| 9 | q4 | abba**[B]** | abba**[B]** | Ambas leram branco → **ACEITA** |
| 10 | **q_aceita** | — | — | ✓ |

**Resultado: ACEITA** — `abba` é palíndromo.

---

## Teste 3 — Entrada: `aabaa` → ACEITA ✓

**Justificativa:** `aabaa` = reverso de `aabaa`, portanto é palíndromo.

*(Rastreamento resumido — 5 símbolos)*

| Passo | Estado | F1[pos] | F2[pos] | Observação |
|-------|--------|---------|---------|------------|
| 0–4 | q0 | cópia | cópia | Fita 2 recebe `aabaa` invertido = `aabaa` |
| 5 | q1→q3 | início | início | Reposicionamento e início de comparação |
| 6–10 | q4 | a=a ✓ | a=a ✓ | Todos os símbolos coincidem |
| 11 | **q_aceita** | B | B | **ACEITA** |

**Resultado: ACEITA**

---

## Teste 4 — Entrada: `ab` → REJEITA ✗

**Justificativa:** reverso de `ab` é `ba` ≠ `ab`.

| Passo | Estado | Fita 1 (cabeça) | Fita 2 (cabeça) | Ação realizada |
|-------|--------|-----------------|-----------------|----------------|
| 0 | q0 | **[a]**b | [B] | Copia 'a'; F1→R, F2→L |
| 1 | q0 | a**[b]** | **[a]** | Copia 'b'; F1→R, F2→L |
| 2 | q1 | ab**[B]** | **[b]**a | Leu branco → avança F2 |
| 3 | q3 | **[a]**b | **[b]**a | F1[0]=a, F2[0]=b → **DIFERENTES** |
| 4 | **q_rejeita** | — | — | ✗ |

**Resultado: REJEITA** — `ab` não é palíndromo.

---

## Teste 5 — Entrada: `aab` → REJEITA ✗

**Justificativa:** reverso de `aab` é `baa` ≠ `aab`.

| Passo | Estado | Fita 1 (cabeça) | Fita 2 (cabeça) | Observação |
|-------|--------|-----------------|-----------------|------------|
| 0–2 | q0 | cópia | cópia | F2 = `baa` (reverso de `aab`) |
| 3 | q3 | **[a]**ab | **[b]**aa | F1[0]=a ≠ F2[0]=b |
| 4 | **q_rejeita** | — | — | ✗ |

**Resultado: REJEITA**

---

## Análise técnica

**Por que este exemplo não é trivial?**
- A máquina usa efetivamente 2 fitas com movimentos independentes
- A Fase 1 exige que Fita 2 se mova para a esquerda enquanto Fita 1 vai para a direita — comportamento impossível em MT de fita única sem overhead de simulação
- O mesmo problema em MT de fita única exigiria O(n²) passos; com 2 fitas é resolvido em O(n)

**Relação com computabilidade:**
- A linguagem dos palíndromos é uma linguagem livre de contexto e também recursiva
- A MT de 2 fitas decide a linguagem (sempre para e responde corretamente)
- Uma MT de fita única equivalente existe, mas com tabela de transição muito maior

**Limitações observadas:**
- O modelo implementado não lida com cadeias de comprimento 0 (string vazia)
- Extensão possível: adicionar tratamento para ε-entrada como palíndromo trivial

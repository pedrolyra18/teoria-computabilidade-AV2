# Rastreamento de Execução — MT com Múltiplas Fitas
**Problema:** Reconhecedor de palíndromo sobre Σ = {a, b}  
**Modelo:** Máquina de Turing com 2 Fitas (Opção 3)

---

## Descrição das fases

| Fase | Estados | Descrição |
|------|---------|-----------|
| Cópia reversa | q0, q1 | Fita 1 lê da esquerda; Fita 2 recebe a cópia invertida |
| Reposicionamento | q2, q3 | As cabeças são alinhadas antes da comparação |
| Comparação | q4, q5, q6, q8 | A igualdade é verificada em estados sucessivos antes da aceitação |
| Decisão | q7 / q8 / q_aceita | q7 trata a cadeia vazia; q8 fecha a comparação; q_aceita encerra a execução |

---

## Teste 1 — Entrada: `aba` → ACEITA ✓

**Justificativa:** `aba` = reverso de `aba`, portanto é palíndromo.

| Passo | Estado | Fita 1 (cabeça) | Fita 2 (cabeça) | Ação realizada |
|-------|--------|-----------------|-----------------|----------------|
| 0 | q0 | **[a]**ba | [B] | Primeiro símbolo: copia e entra em q1 |
| 1 | q1 | a**[b]**a | **[a]** | Continua a cópia reversa |
| 2 | q1 | ab**[a]** | **[b]**a | Continua a cópia reversa |
| 3 | q1 | aba**[B]** | **[a]**ba | Fim da entrada; vai para q2 |
| 4 | q2 | aba**[B]** | **[a]**ba | Avança F2 até o primeiro símbolo |
| 5 | q3 | ab**[a]** | **[a]**ba | Recuo de F1 até alinhar o início |
| 6 | q4 | **[a]**ba | **[a]**ba | Início da comparação |
| 7 | q5 | a**[b]**a | a**[b]**a | F1[1]=b, F2[1]=b ✓ |
| 8 | q6 | ab**[a]** | ab**[a]** | F1[2]=a, F2[2]=a ✓ |
| 9 | q5 | aba**[B]** | aba**[B]** | Ambos em branco → q8 |
| 10 | **q_aceita** | — | — | ✓ |

**Resultado: ACEITA** — `aba` é palíndromo.

---

## Teste 2 — Entrada: `abba` → ACEITA ✓

**Justificativa:** `abba` = reverso de `abba`, portanto é palíndromo.

| Passo | Estado | Fita 1 (cabeça) | Fita 2 (cabeça) | Ação realizada |
|-------|--------|-----------------|-----------------|----------------|
| 0 | q0 | **[a]**bba | [B] | Copia o primeiro símbolo |
| 1 | q1 | a**[b]**ba | **[a]** | Copia o segundo símbolo |
| 2 | q1 | ab**[b]**a | **[b]**a | Copia o terceiro símbolo |
| 3 | q1 | abb**[a]** | **[b]**ba | Copia o quarto símbolo |
| 4 | q1 | abba**[B]** | **[a]**bba | Fim da cópia |
| 5 | q2 | abba**[B]** | **[a]**bba | Reposiciona F2 |
| 6 | q3 | abb**[a]** | **[a]**bba | Reposiciona F1 |
| 7 | q4 | **[a]**bba | **[a]**bba | Compara o primeiro símbolo |
| 8 | q5 | a**[b]**ba | a**[b]**ba | Compara o segundo símbolo |
| 9 | q6 | ab**[b]**a | ab**[b]**a | Mantém a comparação |
| 10 | q6 | abb**[a]** | abb**[a]** | Mantém a comparação |
| 11 | q5 | abba**[B]** | abba**[B]** | Fecha em q8 e aceita |
| 12 | **q_aceita** | — | — | ✓ |

**Resultado: ACEITA** — `abba` é palíndromo.

---

## Teste 3 — Entrada: `aabaa` → ACEITA ✓

**Justificativa:** `aabaa` = reverso de `aabaa`, portanto é palíndromo.

*Rastreamento resumido — 5 símbolos*

| Passo | Estado | F1[pos] | F2[pos] | Observação |
|-------|--------|---------|---------|------------|
| 0–4 | q0→q1 | cópia | cópia | Fita 2 recebe `aabaa` invertido = `aabaa` |
| 5 | q2→q3 | início | início | Reposicionamento das cabeças |
| 6–10 | q4→q5→q6 | a=a ✓ | a=a ✓ | Todos os símbolos coincidem |
| 11 | q8 | B | B | Fecha a comparação |
| 12 | **q_aceita** | B | B | **ACEITA** |

**Resultado: ACEITA**

---

## Teste 4 — Entrada: `ab` → REJEITA ✗

**Justificativa:** reverso de `ab` é `ba` ≠ `ab`.

| Passo | Estado | Fita 1 (cabeça) | Fita 2 (cabeça) | Ação realizada |
|-------|--------|-----------------|-----------------|----------------|
| 0 | q0 | **[a]**b | [B] | Copia o primeiro símbolo |
| 1 | q1 | a**[b]** | **[a]** | Copia o segundo símbolo |
| 2 | q1 | ab**[B]** | **[b]**a | Fim da cópia |
| 3 | q2 | ab**[B]** | **[b]**a | Reposicionamento |
| 4 | q3 | **[a]**b | **[b]**a | Primeira comparação falha → **REJEITA** |

**Resultado: REJEITA** — `ab` não é palíndromo.

---

## Teste 5 — Entrada: `aab` → REJEITA ✗

**Justificativa:** reverso de `aab` é `baa` ≠ `aab`.

| Passo | Estado | Fita 1 (cabeça) | Fita 2 (cabeça) | Observação |
|-------|--------|-----------------|-----------------|------------|
| 0–2 | q0→q1 | cópia | cópia | F2 = `baa` (reverso de `aab`) |
| 3 | q2→q3 | início | início | Reposicionamento |
| 4 | q4 | **[a]**ab | **[b]**aa | F1[0]=a ≠ F2[0]=b |
| 5 | **q_rejeita** | — | — | ✗ |

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

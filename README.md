# AV2 — Teoria da Computabilidade
**Disciplina:** Teoria da Computabilidade  
**Professor:** Daniel Leal Souza  
**Semestre:** 01/2026  
**Turma:** CC5MA / CC5NA  
**Integrantes:** [Nome1], [Nome2], [Nome3], [Nome4]

---

## Modelos escolhidos

| # | Modelo | Opção | Problema resolvido |
|---|--------|-------|--------------------|
| 1 | Máquina de Turing com Múltiplas Fitas | Opção 3 | Reconhecedor de palíndromo sobre {a, b} |
| 2 | Autômato de Pilha (PDA) | Opção 9 | Reconhecedor da linguagem L = {aⁿbⁿ \| n ≥ 1} |

---

## Estrutura do repositório

```
av2-computabilidade/
├── README.md
├── uso_ia.md
├── slides/
│   └── apresentacao.pdf          ← slides da apresentação
├── implementacoes/
│   ├── mt-multifita/
│   │   ├── palindromo.jff         ← arquivo JFLAP (MT 2 fitas)
│   │   └── simulador_mt.py        ← simulador em Python
│   └── pda/
│       ├── anbn.jff               ← arquivo JFLAP (PDA)
│       └── simulador_pda.py       ← simulador em Python
└── testes/
    ├── rastreamento_mt.md         ← rastreamento MT multifita
    └── rastreamento_pda.md        ← rastreamento PDA
```

---

## Como executar

### Requisitos
- Python 3.8+
- Nenhuma dependência externa (biblioteca padrão apenas)
- JFLAP 7.1+ para os arquivos `.jff` → download: https://www.jflap.org

### Simulador MT com Múltiplas Fitas

```bash
python implementacoes/mt-multifita/simulador_mt.py
```

Exemplos de entrada interativa:
```
Digite uma cadeia: aba      → ACEITA
Digite uma cadeia: abba     → ACEITA
Digite uma cadeia: ab       → REJEITA
```

### Simulador PDA (Autômato de Pilha)

```bash
python implementacoes/pda/simulador_pda.py
```

Exemplos de entrada interativa:
```
Digite uma cadeia: aabb     → ACEITA
Digite uma cadeia: aaabbb   → ACEITA
Digite uma cadeia: aab      → REJEITA
```

### Arquivos JFLAP

1. Abra o JFLAP
2. `File → Open` → selecione `palindromo.jff` ou `anbn.jff`
3. `Input → Enter Input` → digite a cadeia de teste
4. Para rastreamento passo a passo: `Input → Step by State`

---

## Referências

- DIVERIO, Tiarajú A.; MENEZES, Paulo B. **Teoria da Computação: Máquinas Universais e Computabilidade.** 3. ed. Porto Alegre: Bookman, 2011.
- MENEZES, Paulo B. **Linguagens Formais e Autômatos.** 6. ed. Porto Alegre: Bookman, 2011.
- Sipser, Michael. **Introduction to the Theory of Computation.** 3. ed. Cengage, 2012.
- Documentação oficial do JFLAP: https://www.jflap.org/jflaptmp/
- Slides da disciplina (Prof. Daniel Leal Souza, CESUPA, 01/2026)

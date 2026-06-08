# AV2 — Teoria da Computabilidade
**Disciplina:** Teoria da Computabilidade  
**Professor:** Daniel Leal Souza  
**Semestre:** 01/2026  
**Turma:** CC5MA / CC5NA  
**Integrantes:** Pedro Lyra, Vithor dos Santos, Murilo Pantoja, João Felipe Soares

## Resumo

Este repositório entrega duas implementações exigidas pela lauda da AV2, com problemas diferentes e rastreamento de execução próprio:

| Modelo | Opção | Problema |
|---|---|---|
| Máquina de Turing com Múltiplas Fitas | Opção 3 | Reconhecimento de palíndromos sobre `{a, b}` |
| Autômato de Pilha (PDA) | Opção 9 | Reconhecimento de `L = {a^n b^n | n >= 1}` |

## Estrutura

- [slides/Apresentação AV2 Teoria da Computabilidade.pdf](slides/Apresentação%20AV2%20Teoria%20da%20Computabilidade.pdf)
- [implementacoes/mt-multifita/simulador_mt.py](implementacoes/mt-multifita/simulador_mt.py)
- [implementacoes/mt-multifita/palindromo.jff](implementacoes/mt-multifita/palindromo.jff)
- [implementacoes/pda/simulador_pda.py](implementacoes/pda/simulador_pda.py)
- [implementacoes/pda/anbn.jff](implementacoes/pda/anbn.jff)
- [testes/rastreamento_mt.md](testes/rastreamento_mt.md)
- [testes/rastreamento_pda.md](testes/rastreamento_pda.md)
- [uso_ia.md](uso_ia.md)

## Execução

Requisitos:

- Python 3.8+
- JFLAP 7.1+ para abrir os `.jff`

Comandos:

```bash
python implementacoes/mt-multifita/simulador_mt.py
python implementacoes/pda/simulador_pda.py
```

No JFLAP, abrir `palindromo.jff` ou `anbn.jff` e usar `Input → Step by State` para acompanhar o rastreamento.

## Entregáveis

O repositório contém os itens pedidos na lauda:

- README com identificação, modelos, execução e referências
- Implementações em Python e JFLAP
- Rastreios de execução em Markdown
- Slides da apresentação
- Declaração de uso de IA

## Referências

- DIVERIO, Tiarajú A.; MENEZES, Paulo B. **Teoria da Computação: Máquinas Universais e Computabilidade.** 3. ed. Porto Alegre: Bookman, 2011.
- MENEZES, Paulo B. **Linguagens Formais e Autômatos.** 6. ed. Porto Alegre: Bookman, 2011.
- SIPSER, Michael. **Introduction to the Theory of Computation.** 3. ed. Cengage, 2012.
- Documentação oficial do JFLAP: https://www.jflap.org/jflaptmp/

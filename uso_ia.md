# Declaração de Uso de Inteligência Artificial

**Disciplina:** Teoria da Computabilidade — AV2  
**Turma:** CC5MA / CC5NA  
**Semestre:** 01/2026  
**Integrantes:** Pedro Lyra, Vithor dos Santos, Murilo Pantoja, João Felipe Soares

---

## Ferramenta utilizada

- **Ferramenta:** GitHub Copilot
- **Modelo:** GPT-5.4 mini
- **Data aproximada de uso:** Junho de 2026

---

## Finalidade do uso

O uso da IA foi restrito às seguintes finalidades:

1. **Apoio na revisão textual** do README, da declaração de uso de IA e dos rastreamentos
2. **Refatoração estrutural** dos simuladores em Python para ampliar o número de estados efetivos
3. **Atualização sincronizada** de arquivos JFLAP `.jff` e documentos Markdown
4. **Sugestão de exemplos de teste** e conferência de rastreamentos, posteriormente verificados manualmente pela equipe
5. **Esclarecimento de dúvidas conceituais** sobre o formato de transições no JFLAP

---

## Resumo dos prompts utilizados e trechos aproveitados

| Prompt utilizado | Trecho aproveitado | Destino |
|------------------|--------------------|---------|
| "Refatore o PDA para usar mais de 8 estados efetivos" | Sugestão de desenrolamento de estados | implementacoes/pda/simulador_pda.py |
| "Refatore a MT multifita para usar mais de 8 estados efetivos" | Sugestão de fases adicionais e comparação repartida | implementacoes/mt-multifita/simulador_mt.py |
| "Atualize os arquivos JFLAP e os rastreamentos" | Estrutura geral das tabelas e rastreamentos | implementacoes/*.jff e testes/*.md |
| "Revise o texto deste README para clareza acadêmica" | Pequenas correções de redação | README.md |

---

## O que foi modificado, corrigido ou rejeitado pela equipe

- A **estrutura final das máquinas** (estados, transições, critérios de aceitação) foi revisada e ajustada pela equipe antes da entrega
- Os **simuladores Python** foram validados com execução real e testes representativos antes de serem mantidos na versão final
- Sugestões de exemplos de teste foram verificadas manualmente em execuções reais no Python/JFLAP antes de serem incluídas nos rastreamentos
- Explicações conceituais e referências foram contrastadas com o livro-texto (Diverio & Menezes, 2011) e com os slides da disciplina

---

## Declaração

Todos os integrantes da equipe leram, revisaram e **compreendem integralmente** o conteúdo deste trabalho, incluindo os trechos em que houve apoio de IA. A IA foi utilizada como ferramenta de apoio, não como substituta do estudo, da implementação ou do domínio conceitual exigido pela atividade.



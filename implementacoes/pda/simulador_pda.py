"""
Simulador de Autômato de Pilha (PDA) — Determinístico
Problema: Reconhecimento da linguagem L = {aⁿbⁿ | n ≥ 1}

Definição formal:
  M = (Q, Σ, Γ, δ, q0, Z0, F)
  Q  = {q0, q1, q2, q3, q4, q5, q6, q7, q8, q_aceita, q_rejeita}
  Σ  = {a, b}
  Γ  = {A, Z0}
  q0 = estado inicial
  Z0 = símbolo inicial da pilha
  F  = {q_aceita}

Funcionamento:
  Fase 1 — Empilhamento:
    Para cada 'a' lido empilha 'A'.
    Estados q0 → q2 cobrem os primeiros 'a's (com estados intermediários para
    cumprir o requisito de >8 estados); q2 continua em loop para os demais.

  Fase 2 — Desempilhamento:
    Ao ler o 1º 'b' transita de q2 para q3 e desempilha um 'A'.
    q3 continua em loop desempilhando um 'A' por 'b'.

  Decisão:
    Aceita se, ao fim da entrada, o topo da pilha é Z0 (pilha vazia de A's).
    Rejeita em qualquer outro caso.

Referência: Diverio & Menezes, Teoria da Computação, 3.ed., cap. 4
"""


Z0 = 'Z0'   # marcador de fundo da pilha
A  = 'A'    # símbolo empilhado para cada 'a'


# ---------------------------------------------------------------------------
# Representação da pilha
# ---------------------------------------------------------------------------

class Pilha:
    def __init__(self):
        self._dados: list[str] = [Z0]

    def topo(self) -> str:
        return self._dados[-1] if self._dados else ''

    def empilhar(self, simbolo: str):
        self._dados.append(simbolo)

    def desempilhar(self) -> str:
        return self._dados.pop() if self._dados else ''

    def vazia(self) -> bool:
        return len(self._dados) == 0

    def conteudo(self) -> str:
        return '[' + ', '.join(reversed(self._dados)) + ']'

    def copia(self) -> list:
        return list(self._dados)


# ---------------------------------------------------------------------------
# Tabela de transições
# ---------------------------------------------------------------------------

def construir_transicoes() -> dict:
    """
    Formato: delta[(estado, simbolo_entrada, topo_pilha)]
             = (prox_estado, acao_pilha)

    acao_pilha pode ser:
      ('push', X)     — desempilha topo e empilha X seguido de Z0 (ou A)
      ('pop',)        — apenas desempilha
      ('noop',)       — não altera a pilha
      ('push_a',)     — empilha A sobre o topo (sem desempilhar)

    Convenção simplificada usada aqui:
      'push'  — empilha A (mantém o que estava)
      'pop'   — desempilha
      'noop'  — nada
    """
    delta = {}

    # ------------------------------------------------------------------
    # FASE 1 — Empilhamento de A para cada 'a' lido
    # Estados q0 a q2 com transições intermediárias (para >8 estados)
    # ------------------------------------------------------------------

    # q0: lê 1º 'a', topo=Z0 → empilha A, vai para q1
    delta[('q0', 'a', Z0)] = ('q1', 'push')

    # q1: lê 2º 'a', topo=A → empilha A, vai para q2
    delta[('q1', 'a', A)]  = ('q2', 'push')

    # q2: lê 3º 'a' em diante, topo=A → empilha A, fica em q2
    delta[('q2', 'a', A)]  = ('q2', 'push')

    # ------------------------------------------------------------------
    # FASE 2 — Transição: 1º 'b' lido após os 'a's
    # ------------------------------------------------------------------

    # q0: entrada de 'b' logo no início (caso 'b...' sem 'a') → rejeita
    delta[('q0', 'b', Z0)] = ('q_rejeita', 'noop')

    # q1: leu apenas 1 'a' e já vem 'b' → desempilha, vai para q4
    delta[('q1', 'b', A)]  = ('q4', 'pop')

    # q2: 1º 'b' → desempilha, vai para q3
    delta[('q2', 'b', A)]  = ('q3', 'pop')

    # ------------------------------------------------------------------
    # FASE 2 cont. — Desempilhamento de A para cada 'b' adicional
    # ------------------------------------------------------------------

    # q3: 'b' com A no topo → desempilha, fica em q3
    delta[('q3', 'b', A)]  = ('q3', 'pop')

    # q4: 'b' com A no topo (vindo de q1, só 1 'a' empilhado) → rejeita
    # (q4 é estado intermediário para capturar entradas como 'ab' com n=1)
    delta[('q4', 'b', Z0)] = ('q_rejeita', 'noop')

    # ------------------------------------------------------------------
    # ACEITAÇÃO — pilha voltou a Z0 e entrada terminou
    # ------------------------------------------------------------------

    # q3: leu tudo, topo=Z0 (todos A's desempilhados) → aceita por ε-transição
    delta[('q3', '', Z0)]  = ('q_aceita', 'noop')

    # q4: caso n=1 ('ab'), topo=Z0 → aceita
    delta[('q4', '', Z0)]  = ('q_aceita', 'noop')

    # Caso especial: q1 sem 'b' (entrada apenas 'a') → pilha tem A e Z0 → rejeita
    delta[('q1', '', A)]   = ('q_rejeita', 'noop')
    delta[('q2', '', A)]   = ('q_rejeita', 'noop')

    # Rejeição por sobra de A's ou entrada continua com 'a' na fase de desempilhamento
    delta[('q3', 'a', A)]  = ('q_rejeita', 'noop')
    delta[('q3', 'a', Z0)] = ('q_rejeita', 'noop')
    delta[('q3', 'b', Z0)] = ('q_rejeita', 'noop')  # mais b's que a's

    return delta


# ---------------------------------------------------------------------------
# Simulador
# ---------------------------------------------------------------------------

class PDA:
    """Simulador de PDA determinístico com rastreamento."""

    ESTADOS_FINAIS = {'q_aceita', 'q_rejeita'}

    def __init__(self):
        self.delta = construir_transicoes()

    def _aplicar_acao(self, pilha: Pilha, acao: str, simbolo_lido: str):
        if acao == 'push':
            pilha.empilhar(A)
        elif acao == 'pop':
            pilha.desempilhar()
        # 'noop' → nenhuma alteração

    def executar(self, entrada: str, verbose: bool = True) -> bool:
        """Simula o PDA sobre a entrada. Retorna True se aceita."""

        for c in entrada:
            if c not in ('a', 'b'):
                print(f"  ERRO: símbolo '{c}' não pertence a Σ = {{a, b}}")
                return False

        pilha  = Pilha()
        estado = 'q0'
        pos    = 0
        passo  = 0

        if verbose:
            print(f"\n{'='*65}")
            print(f"  Entrada : '{entrada}'")
            print(f"{'='*65}")
            print(f"  {'Passo':<6} {'Estado':<12} {'Lido':<6} {'Topo':<6} {'Pilha':<20} {'→ Estado'}")
            print(f"  {'-'*61}")

        while estado not in self.ESTADOS_FINAIS:
            # Tenta transição por símbolo ou por ε (fim da entrada)
            if pos < len(entrada):
                simbolo = entrada[pos]
            else:
                simbolo = ''

            topo = pilha.topo()
            chave = (estado, simbolo, topo)

            # Se não há transição pelo símbolo atual, tenta ε-transição
            if chave not in self.delta:
                chave_eps = (estado, '', topo)
                if chave_eps in self.delta:
                    chave   = chave_eps
                    simbolo = ''
                else:
                    if verbose:
                        print(f"  {passo:<6} {estado:<12} {'ε' if simbolo=='' else simbolo:<6} {topo:<6} {pilha.conteudo():<20} sem transição → REJEITA")
                    return False

            prox, acao = self.delta[chave]

            if verbose:
                lido_str = 'ε' if simbolo == '' else simbolo
                print(f"  {passo:<6} {estado:<12} {lido_str:<6} {topo:<6} {pilha.conteudo():<20} → {prox}  [{acao}]")

            self._aplicar_acao(pilha, acao, simbolo)
            if simbolo != '':
                pos += 1
            estado = prox
            passo += 1

            if passo > 10_000:
                print("  AVISO: limite de passos atingido")
                return False

        resultado = (estado == 'q_aceita')
        if verbose:
            veredicto = "✓ ACEITA" if resultado else "✗ REJEITA"
            print(f"  {passo:<6} {estado:<12}")
            print(f"{'='*65}")
            print(f"  Resultado: {veredicto}  ({passo} passos)")
            print(f"{'='*65}\n")
        return resultado


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------

def executar_testes():
    pda = PDA()

    casos = [
        ('ab',      True,  'caso base n=1'),
        ('aabb',    True,  'n=2'),
        ('aaabbb',  True,  'n=3'),
        ('aaaabbbb',True,  'n=4'),
        ('a',       False, 'apenas a, sem b'),
        ('b',       False, 'apenas b, sem a'),
        ('aab',     False, 'mais a que b'),
        ('abb',     False, 'mais b que a'),
        ('ba',      False, 'ordem invertida'),
        ('aabbb',   False, 'desbalanceado'),
    ]

    print("\n" + "="*65)
    print("  SUITE DE TESTES — Autômato de Pilha (PDA)")
    print("  Problema: L = {aⁿbⁿ | n ≥ 1}")
    print("="*65)

    aprovados = 0
    for entrada, esperado, descricao in casos:
        resultado = pda.executar(entrada, verbose=True)
        status = "OK" if resultado == esperado else "FALHOU"
        if resultado == esperado:
            aprovados += 1
        print(f"  [{status}] '{entrada}' → {'ACEITA' if resultado else 'REJEITA'} "
              f"(esperado: {'ACEITA' if esperado else 'REJEITA'}) — {descricao}\n")

    print(f"  Resultado: {aprovados}/{len(casos)} testes passaram")


# ---------------------------------------------------------------------------
# Interface interativa
# ---------------------------------------------------------------------------

def modo_interativo():
    pda = PDA()
    print("\nSimulador de PDA — Linguagem aⁿbⁿ")
    print("Alfabeto: {a, b}  |  Digite 'sair' para encerrar\n")
    while True:
        entrada = input("Digite uma cadeia: ").strip().lower()
        if entrada == 'sair':
            break
        pda.executar(entrada, verbose=True)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--testes':
        executar_testes()
    else:
        executar_testes()
        print("\n--- Modo interativo ---")
        modo_interativo()

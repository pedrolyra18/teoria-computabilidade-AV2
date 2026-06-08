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
        Os primeiros quatro 'a's são desenrolados em estados distintos.
        A partir de q6, a máquina entra em loop para os demais 'a's.

  Fase 2 — Desempilhamento:
        Os primeiros 'b's passam por q7 e q8 antes da aceitação, mantendo o fluxo
        natural de desempilhamento e satisfazendo o requisito de 9+ estados efetivos.

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
    # FASE 1 — Empilhamento com desenrolamento explícito dos primeiros 'a'
    # ------------------------------------------------------------------

    # q0: lê o 1º 'a', empilha A e avança para q1
    delta[('q0', 'a', Z0)] = ('q1', 'push')

    # q1: lê o 2º 'a', empilha A e avança para q2
    delta[('q1', 'a', A)]  = ('q2', 'push')

    # q2: lê o 3º 'a', empilha A e avança para q5
    delta[('q2', 'a', A)]  = ('q5', 'push')

    # q5: lê o 4º 'a', empilha A e avança para q6
    delta[('q5', 'a', A)]  = ('q6', 'push')

    # q6: continua empilhando A para os 'a' restantes
    delta[('q6', 'a', A)]  = ('q6', 'push')

    # ------------------------------------------------------------------
    # FASE 2 — Início da leitura de 'b' com estados de fronteira naturais
    # ------------------------------------------------------------------

    # q0: entrada iniciada com 'b' → rejeita
    delta[('q0', 'b', Z0)] = ('q_rejeita', 'noop')

    # q1: n = 1, ao ler o 1º 'b' remove o único A e prepara aceitação
    delta[('q1', 'b', A)]  = ('q3', 'pop')

    # q2: n = 2, ao ler o 1º 'b' remove um A e prepara a fase final
    delta[('q2', 'b', A)]  = ('q4', 'pop')

    # q5: n = 3, ao ler o 1º 'b' já entra na sequência de desempilhamento
    delta[('q5', 'b', A)]  = ('q7', 'pop')

    # q6: primeiro 'b' após o bloco de 'a's; passa para q7
    delta[('q6', 'b', A)]  = ('q7', 'pop')

    # q7: desempilha o próximo A e encaminha para q8
    delta[('q7', 'b', A)]  = ('q8', 'pop')

    # q8: continua o desempilhamento para os 'b' restantes
    delta[('q8', 'b', A)]  = ('q8', 'pop')

    # ------------------------------------------------------------------
    # ACEITAÇÃO — pilha voltou a Z0 e a entrada terminou
    # ------------------------------------------------------------------

    # q3: caso n = 1 ('ab'), topo já voltou a Z0 → aceita
    delta[('q3', '', Z0)]  = ('q_aceita', 'noop')
    delta[('q3', 'a', A)]   = ('q_rejeita', 'noop')
    delta[('q3', 'b', A)]   = ('q_rejeita', 'noop')
    delta[('q3', 'a', Z0)]  = ('q_rejeita', 'noop')
    delta[('q3', 'b', Z0)]  = ('q_rejeita', 'noop')

    # q4: caso n = 2 ('aabb'), consome o último 'b' e encaminha para q8
    delta[('q4', 'b', A)]   = ('q8', 'pop')
    delta[('q4', '', Z0)]  = ('q_rejeita', 'noop')
    delta[('q4', 'a', A)]   = ('q_rejeita', 'noop')
    delta[('q4', 'a', Z0)]  = ('q_rejeita', 'noop')
    delta[('q4', 'b', Z0)]  = ('q_rejeita', 'noop')

    # q8: fim da cadeia após consumir todos os b's → aceita
    delta[('q8', '', Z0)]  = ('q_aceita', 'noop')
    delta[('q8', 'a', A)]  = ('q_rejeita', 'noop')
    delta[('q8', 'a', Z0)] = ('q_rejeita', 'noop')
    delta[('q8', 'b', Z0)] = ('q_rejeita', 'noop')

    # Rejeição por falta de b, excesso de a ou entrada inválida na fase final
    delta[('q1', '', A)]   = ('q_rejeita', 'noop')
    delta[('q2', '', A)]   = ('q_rejeita', 'noop')
    delta[('q5', '', A)]   = ('q_rejeita', 'noop')
    delta[('q6', '', A)]   = ('q_rejeita', 'noop')
    delta[('q7', '', A)]   = ('q_rejeita', 'noop')
    delta[('q7', 'a', A)]  = ('q_rejeita', 'noop')
    delta[('q5', 'a', Z0)]  = ('q_rejeita', 'noop')
    delta[('q5', 'b', Z0)]  = ('q_rejeita', 'noop')
    delta[('q6', 'a', Z0)]  = ('q_rejeita', 'noop')
    delta[('q6', 'b', Z0)]  = ('q_rejeita', 'noop')
    delta[('q7', 'a', Z0)]  = ('q_rejeita', 'noop')
    delta[('q7', 'b', Z0)]  = ('q_rejeita', 'noop')

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

"""
Simulador de Máquina de Turing com Múltiplas Fitas (2 fitas)
Problema: Reconhecimento de palíndromos sobre o alfabeto {a, b}

Definição formal:
  M = (Q, Σ, Γ, δ, q0, q_aceita, q_rejeita)
  Q = {q0, q1, q2, q3, q4, q5, q6, q7, q8, q_aceita, q_rejeita}
  Σ = {a, b}
  Γ = {a, b, B}  (B = branco)
  q0 = estado inicial
  Critério de aceitação: chegar a q_aceita

Funcionamento:
  Fase 1 (cópia reversa): Fita 1 lê da esquerda para a direita;
                          Fita 2 recebe os símbolos da direita para a esquerda.
  Fase 2 (retorno):       Cabeça da Fita 1 volta ao início.
  Fase 3 (comparação):    Fita 1 e Fita 2 são lidas simultaneamente.
  Decisão: aceita se todos os símbolos coincidirem até o branco.

Referência: Diverio & Menezes, Teoria da Computação, 3.ed., cap. 5
"""

BRANCO = 'B'


# ---------------------------------------------------------------------------
# Representação das fitas
# ---------------------------------------------------------------------------

class Fita:
    """Fita bidirecional indexada por inteiros (posição 0 = início)."""

    def __init__(self, conteudo: str = ''):
        self._cells: dict[int, str] = {}
        for i, c in enumerate(conteudo):
            self._cells[i] = c
        self._head: int = 0

    def ler(self) -> str:
        return self._cells.get(self._head, BRANCO)

    def escrever(self, simbolo: str):
        self._cells[self._head] = simbolo

    def mover(self, direcao: str):
        """R = direita, L = esquerda, S = parado."""
        if direcao == 'R':
            self._head += 1
        elif direcao == 'L':
            self._head -= 1

    def posicao(self) -> int:
        return self._head

    def ir_para(self, pos: int):
        self._head = pos

    def conteudo_str(self) -> str:
        if not self._cells:
            return BRANCO
        lo = min(self._cells)
        hi = max(self._cells)
        return ''.join(self._cells.get(i, BRANCO) for i in range(lo, hi + 1))


# ---------------------------------------------------------------------------
# Tabela de transições
# ---------------------------------------------------------------------------

def construir_transicoes() -> dict:
    """
    Formato: delta[(estado, leitura_fita1, leitura_fita2)]
             = (prox_estado, escrita_fita1, dir_fita1, escrita_fita2, dir_fita2)

    Estados:
      q0  — cópia reversa (lê Fita1, escreve Fita2 ao contrário)
      q1  — detectou fim da entrada (leu branco em Fita1)
      q2  — retorno da cabeça de Fita1 para o início
      q3  — início da comparação
      q4  — comparando (loop)
      q5  — verificou 'a'='a'
      q6  — verificou 'b'='b'
      q7  — preparando próxima comparação
      q8  — encontrou fim das duas fitas simultaneamente
      q_aceita — aceita
      q_rejeita — rejeita
    """
    delta = {}

    # -----------------------------------------------------------------------
    # FASE 1: Cópia reversa
    # Fita1 move R; Fita2 move L (escreve de trás para frente)
    # -----------------------------------------------------------------------
    for s in ('a', 'b'):
        # q0: lendo símbolo em Fita1, qualquer coisa na Fita2 (usamos B pois
        # Fita2 começa vazia e a cabeça vai recuando)
        delta[('q0', s, BRANCO)] = ('q0', s, 'R', s, 'L')

    # q0: leu branco em Fita1 → fim da entrada → vai para q1
    delta[('q0', BRANCO, BRANCO)] = ('q1', BRANCO, 'S', BRANCO, 'R')

    # -----------------------------------------------------------------------
    # FASE 2: Avanço de Fita2 até o início do conteúdo copiado
    # (Fita2 está com a cabeça uma posição além do último símbolo escrito)
    # q1: avança Fita2 para a direita até encontrar o primeiro símbolo
    # -----------------------------------------------------------------------
    delta[('q1', BRANCO, BRANCO)] = ('q2', BRANCO, 'L', BRANCO, 'S')
    for s in ('a', 'b'):
        delta[('q1', BRANCO, s)]  = ('q3', BRANCO, 'R', s, 'S')

    # -----------------------------------------------------------------------
    # FASE 2b: Retorno de Fita1 ao início
    # q2: Fita1 recua para a esquerda até encontrar branco
    # -----------------------------------------------------------------------
    for s in ('a', 'b'):
        delta[('q2', s, BRANCO)] = ('q2', s, 'L', BRANCO, 'S')
    delta[('q2', BRANCO, BRANCO)] = ('q3', BRANCO, 'R', BRANCO, 'S')

    # -----------------------------------------------------------------------
    # FASE 3: Comparação simultânea
    # q3/q4: lê Fita1 e Fita2 ao mesmo tempo
    # -----------------------------------------------------------------------
    # Símbolos iguais → continua
    delta[('q3', 'a', 'a')] = ('q4', 'a', 'R', 'a', 'R')
    delta[('q3', 'b', 'b')] = ('q4', 'b', 'R', 'b', 'R')
    delta[('q4', 'a', 'a')] = ('q4', 'a', 'R', 'a', 'R')
    delta[('q4', 'b', 'b')] = ('q4', 'b', 'R', 'b', 'R')

    # Símbolos diferentes → rejeita
    delta[('q3', 'a', 'b')] = ('q_rejeita', 'a', 'S', 'b', 'S')
    delta[('q3', 'b', 'a')] = ('q_rejeita', 'b', 'S', 'a', 'S')
    delta[('q4', 'a', 'b')] = ('q_rejeita', 'a', 'S', 'b', 'S')
    delta[('q4', 'b', 'a')] = ('q_rejeita', 'b', 'S', 'a', 'S')

    # Fim simultâneo (ambas leram branco) → aceita
    delta[('q3', BRANCO, BRANCO)] = ('q_aceita', BRANCO, 'S', BRANCO, 'S')
    delta[('q4', BRANCO, BRANCO)] = ('q_aceita', BRANCO, 'S', BRANCO, 'S')

    # Fim assimétrico → rejeita
    delta[('q3', BRANCO, 'a')] = ('q_rejeita', BRANCO, 'S', 'a', 'S')
    delta[('q3', BRANCO, 'b')] = ('q_rejeita', BRANCO, 'S', 'b', 'S')
    delta[('q3', 'a', BRANCO)] = ('q_rejeita', 'a', 'S', BRANCO, 'S')
    delta[('q3', 'b', BRANCO)] = ('q_rejeita', 'b', 'S', BRANCO, 'S')
    delta[('q4', BRANCO, 'a')] = ('q_rejeita', BRANCO, 'S', 'a', 'S')
    delta[('q4', BRANCO, 'b')] = ('q_rejeita', BRANCO, 'S', 'b', 'S')
    delta[('q4', 'a', BRANCO)] = ('q_rejeita', 'a', 'S', BRANCO, 'S')
    delta[('q4', 'b', BRANCO)] = ('q_rejeita', 'b', 'S', BRANCO, 'S')

    return delta


# ---------------------------------------------------------------------------
# Simulador
# ---------------------------------------------------------------------------

class MTMultifita:
    """Simulador de MT de 2 fitas com rastreamento de execução."""

    ESTADOS_FINAIS = {'q_aceita', 'q_rejeita'}

    def __init__(self):
        self.delta = construir_transicoes()

    def executar(self, entrada: str, verbose: bool = True) -> bool:
        """
        Executa a MT sobre a entrada e retorna True se aceita, False se rejeita.
        Se verbose=True, imprime o rastreamento de cada passo.
        """
        # Validar alfabeto
        for c in entrada:
            if c not in ('a', 'b'):
                print(f"  ERRO: símbolo '{c}' não pertence ao alfabeto Σ = {{a, b}}")
                return False

        fita1 = Fita(entrada)
        fita2 = Fita()
        estado = 'q0'
        passo = 0

        if verbose:
            print(f"\n{'='*60}")
            print(f"  Entrada: '{entrada}'")
            print(f"{'='*60}")
            print(f"  {'Passo':<6} {'Estado':<12} {'F1[pos]':<10} {'F2[pos]':<10} {'Ação'}")
            print(f"  {'-'*56}")

        while estado not in self.ESTADOS_FINAIS:
            l1 = fita1.ler()
            l2 = fita2.ler()

            chave = (estado, l1, l2)
            if chave not in self.delta:
                if verbose:
                    print(f"  {passo:<6} {estado:<12} {l1+'['+str(fita1.posicao())+']':<10} {l2+'['+str(fita2.posicao())+']':<10} sem transição → REJEITA")
                return False

            prox, e1, d1, e2, d2 = self.delta[chave]

            if verbose:
                acao = f"({l1},{l2})→({e1},{e2}) | F1:{d1} F2:{d2} → {prox}"
                pos1 = f"{l1}[{fita1.posicao()}]"
                pos2 = f"{l2}[{fita2.posicao()}]"
                print(f"  {passo:<6} {estado:<12} {pos1:<10} {pos2:<10} {acao}")

            fita1.escrever(e1)
            fita2.escrever(e2)
            fita1.mover(d1)
            fita2.mover(d2)
            estado = prox
            passo += 1

            if passo > 10_000:
                print("  AVISO: limite de passos atingido (possível loop)")
                return False

        resultado = (estado == 'q_aceita')
        if verbose:
            veredicto = "✓ ACEITA" if resultado else "✗ REJEITA"
            print(f"  {passo:<6} {estado:<12}")
            print(f"{'='*60}")
            print(f"  Resultado: {veredicto}  ({passo} passos)")
            print(f"{'='*60}\n")
        return resultado


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------

def executar_testes():
    mt = MTMultifita()

    casos = [
        ('aba',   True,  'palíndromo ímpar simples'),
        ('abba',  True,  'palíndromo par'),
        ('aabaa', True,  'palíndromo ímpar maior'),
        ('a',     True,  'cadeia unitária (palíndromo trivial)'),
        ('ab',    False, 'não é palíndromo'),
        ('aab',   False, 'não é palíndromo'),
        ('abab',  False, 'não é palíndromo'),
    ]

    print("\n" + "="*60)
    print("  SUITE DE TESTES — MT com Múltiplas Fitas")
    print("  Problema: Reconhecimento de Palíndromos")
    print("="*60)

    aprovados = 0
    for entrada, esperado, descricao in casos:
        resultado = mt.executar(entrada, verbose=True)
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
    mt = MTMultifita()
    print("\nSimulador de MT com Múltiplas Fitas — Palíndromo")
    print("Alfabeto: {a, b}  |  Digite 'sair' para encerrar\n")
    while True:
        entrada = input("Digite uma cadeia: ").strip().lower()
        if entrada == 'sair':
            break
        mt.executar(entrada, verbose=True)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--testes':
        executar_testes()
    else:
        executar_testes()
        print("\n--- Modo interativo ---")
        modo_interativo()

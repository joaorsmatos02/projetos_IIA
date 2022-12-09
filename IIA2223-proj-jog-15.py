# João Matos 56292
# Tomás Barreto 56282
# Diogo Pereira 56302

from jogos import *
from utils import *
from copy import deepcopy
import sys

EstadoJogo_15 = namedtuple('EstadoJogo_15',['to_move', 'white', 'black'])

class JogoBT_15(Game):

    # Construtor da classe
    def __init__(self, n=8):
        self.initial = EstadoJogo_15(1, [('a',1),('b',1),('c',1),('d',1),('e',1),('f',1),('g',1),('h',1),
                                      ('a',2),('b',2),('c',2),('d',2),('e',2),('f',2),('g',2),('h',2) ],
                                     [('a',n-1),('b',n-1),('c',n-1),('d',n-1),('e',n-1),('f',n-1),('g',n-1),('h',n-1),
                                      ('a',n),('b',n),('c',n),('d',n),('e',n),('f',n),('g',n),('h',n)], )
        self.size = n

    # Ações possiveis, dado um estado
    def actions(self, state):
        mov = list()

        # verificar se o jogo acabou
        if self.terminal_test(state):
            return mov

        if state.to_move == 1:
            keys = state.white
            dir = 1
        else:
            keys = state.black
            dir = -1

        for key in keys:
            # se nao acabou ver movimentos
            top = (key[0], key[1] + dir)
            topRight = (chr((ord(key[0]) + dir)), key[1] + dir)
            topLeft = (chr((ord(key[0]) - dir)), key[1] + dir)
            if ((dir == 1 and key[1] != self.size) or (dir == -1 and key[1] != 1)) and top not in state.white and top not in state.black: # None pq nao pode comer para a frente
                mov.append("{0}{1}-{2}{3}".format(key[0],key[1],top[0],top[1]))
            if ((dir == 1 and key[0] != 'a') or (dir == -1 and key[0] != 'h')) and topLeft not in keys:
                mov.append("{0}{1}-{2}{3}".format(key[0],key[1],topLeft[0],topLeft[1]))
            if ((dir == 1 and key[0] != 'h') or (dir == -1 and key[0] != 'a')) and topRight not in keys:
                mov.append("{0}{1}-{2}{3}".format(key[0],key[1],topRight[0],topRight[1]))

        return sorted(mov)

    # Verifica se o jogo acabou
    def terminal_test(self, state):
        for key in state.white:
            if key[1] == self.size:
                return True
        for key in state.black:
            if key[1] == 1:
                return True
        return False

    # Resultado da aplicação de move em state
    def result(self, state, move):
        newWhite = deepcopy(state.white)
        newBlack = deepcopy(state.black)

        newPos = (move[3], int(move[4]))
        oldPos = (move[0], int(move[1]))
        if oldPos in newWhite:
            if newPos in newBlack:
                newBlack.remove(newPos)
            newWhite.remove(oldPos)
            newWhite.append(newPos)
        else:
            if newPos in newWhite:
                newWhite.remove(newPos)
            newBlack.remove(oldPos)
            newBlack.append(newPos)

        if state.to_move == 1:
            return EstadoJogo_15(2, newWhite, newBlack)
        else:
            return EstadoJogo_15(1, newWhite, newBlack)

    # Imprime o tabuleiro state
    def display(self, state):
        alpha = "abcdefgh"
        print("-----------------")

        for i in range(self.size,0,-1):
            print("{}|".format(i), end="")
            for j in range(0,self.size):
                j = alpha[j]
                if (j,i) in state.white:
                    print('W', end="")
                elif (j,i) in state.black:
                    print('B', end="")
                else:
                    print(".", end="")
                print(" ", end="")
            print()

        print("-+---------------")
        print(" |a b c d e f g h")

        if not self.terminal_test(state):
            if state[0] == 1:
                char = 'W'
            else:
                char = 'B'
            print("--NEXT PLAYER:", char)

    # Executa a sequência de ações especificada
    def executa(self, state, actions):
        s = state
        for j in actions:
            s = self.result(s, j)
        return s

    # Calcula o score para o jogador indicado
    def utility(self, state, player):
        white = map(lambda n : n[1], state.white)
        black = map(lambda n : n[1], state.black)
        if (player == 1 and 8 in white) or \
            (player == 2 and 1 in black):
            return 1
        elif (player == 1 and 1 in black) or \
             (player == 2 and 8 in white):
            return -1
        else:
            return 0

###############################################################################
################################## FUNÇÃO #####################################
###############################################################################

# procura manter linhas defensivas e nao valoriza tanto a pos individual de cada peça
def func_aval_15(estado, jogador):
    alphabet = "abcdefgh"
    lines = [[(a,b) for a in alphabet] for b in range(2,8)]
    s = 0
    if jogador == 1:
        ourPieces = estado.white
        otherPieces = estado.black
    else:
        ourPieces = estado.black
        otherPieces = estado.white
    lowest = 0
    highest = 0
    for key in ourPieces:

        if jogador == 1: # se for peças brancas

            if key[1] == 8:
                return sys.maxsize # se puder ganhar atribuir score maximo

            # incentivar a mover peças aos pares
            if (key[0], key[1] + 1) in ourPieces or (key[0], key[1] - 1) in ourPieces:
                s += key[1]**key[1]

            if lowest == 0: # guardar a pos mais atrasada
                lowest = key[1]
            else: 
                lowest = min(lowest, key[1])

            # verificar posicoes protegidas
            x = alphabet.index(key[0])
            if key[1] > 1 and key[1] < 7 and key in lines[key[1] - 2]:
                lines[key[1] - 2].remove(key)
            if key[1] < 7:
                if x == 7 and (alphabet[x-1], key[1] + 1) in lines[key[1] - 1]:
                    lines[key[1] - 1].remove((alphabet[x-1], key[1] + 1))
                if x == 0 and (alphabet[x+1], key[1] + 1) in lines[key[1] - 1]:
                    lines[key[1] - 1].remove((alphabet[x+1], key[1] + 1))
                if x != 7 and (alphabet[x+1], key[1] + 1) in lines[key[1] - 1]:
                    lines[key[1] - 1].remove((alphabet[x+1], key[1] + 1))
                if x != 0 and (alphabet[x-1], key[1] + 1) in lines[key[1] - 1]: 
                    lines[key[1] - 1].remove((alphabet[x-1], key[1] + 1))
        
            # verifiar se pode ser comida na proxima
            if (x == 7 and (alphabet[x-1], key[1] + 1) in otherPieces) or \
               (x == 0 and (alphabet[x+1], key[1] + 1) in otherPieces) or \
               (x != 7 and (alphabet[x+1], key[1] + 1) in otherPieces) or \
               (x != 0 and (alphabet[x-1], key[1] + 1) in otherPieces): 

                s += key[1]**key[1] / 4
            else:
                s += key[1]**key[1]

        else: # se for peças pretas

            if key[1] == 1:
                return sys.maxsize # se puder ganhar atribuir score maximo

            # incentivar a mover peças aos pares
            if (key[0], key[1] + 1) in ourPieces or (key[0], key[1] - 1) in ourPieces:
                s += (9-key[1])**(9-key[1])

            if lowest == 0: # guardar a pos mais atrasada
                lowest = key[1]
            else: 
                lowest = max(lowest, key[1])

            # verificar posicoes protegidas
            x = alphabet.index(key[0]) 
            if key[1] > 1 and key[1] < 7 and key in lines[key[1] - 2]:
                lines[key[1] - 2].remove(key)
            if key[1] > 2:    
                if x == 7 and (alphabet[x-1], key[1] - 1) in lines[key[1] - 3]:
                    lines[key[1] - 3].remove((alphabet[x-1], key[1] - 1))
                if x == 0 and (alphabet[x+1], key[1] - 1) in lines[key[1] - 3]:
                    lines[key[1] - 3].remove((alphabet[x+1], key[1] - 1))
                if x != 7 and (alphabet[x+1], key[1] - 1) in lines[key[1] - 3]:
                    lines[key[1] - 3].remove((alphabet[x+1], key[1] - 1))
                if x != 0 and (alphabet[x-1], key[1] - 1) in lines[key[1] - 3]: 
                    lines[key[1] - 3].remove((alphabet[x-1], key[1] - 1))

            # verificar se pode ser comida na proxima
            if (x == 7 and (alphabet[x-1], key[1] - 1) in otherPieces) or \
               (x == 0 and (alphabet[x+1], key[1] - 1) in otherPieces) or \
               (x != 7 and (alphabet[x+1], key[1] - 1) in otherPieces) or \
               (x != 0 and (alphabet[x-1], key[1] - 1) in otherPieces): 

                s += (9-key[1])**(9-key[1]) / 4
            else:
                s += (9-key[1])**(9-key[1])

    for key in otherPieces:
        # se ultima linha de defesa tiver sido ultrapassada
        if (jogador == 1 and key[1] == 1) or (jogador != 1 and key[1] == 8) or key[1] == lowest:
            return -sys.maxsize

        if highest == 0: 
            highest = key[1]
        if jogador != 1: # guardar a pos mais adiantada do adversario            
            highest = max(highest, key[1])
        else:
            highest = min(highest, key[1])            

        if jogador == 1:
            s -= (9-key[1])**(9-key[1])
        else:
            s -= key[1]**key[1]

    for line in range(1,len(lines) + 1): # contar o numero de linhas totalmente defendidas
        if ((jogador == 1 and line < highest) or (jogador != 1 and line > highest)) and len(lines[line - 1]) == 0: # dar pontos por cada linha protegida
            if jogador == 1:
                s += (9-line)**(9-line) * 3
            else:
                s += line**line * 3

    return s
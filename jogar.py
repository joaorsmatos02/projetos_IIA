##Versão 14 Nov 2022 11:19

        
from random import *

##################################
# Classe Jogador 

class Jogador():
    def __init__(self, nome, fun):
        self.nome = nome
        self.fun = fun
    def display(self):
        print(self.nome+" ")


# Classe JogadorAlfaBeta 

class JogadorAlfaBeta(Jogador):
    def __init__(self, nome, depth,fun_eval):
        self.nome = nome
        self.fun = lambda game, state: alphabeta_cutoff_search_new(state,game,depth,eval_fn=fun_eval)
    def display(self):
        print(self.nome+" ")


from jogos import *

##########  para ser independente dos jogos deveria devolver um método em string ou um atributo
def joga11(game, jog1, jog2):
    ### jog1 e jog2 são jogadores com funções que dado um estado do jogo devolvem a jogada que escolheram
    ### devolve uma lista de jogadas e o resultado 1 se Brancas ganha -1 se Pretas ganha
    estado=game.initial
    proxjog = jog1
    lista_jogadas=[]
    while not game.terminal_test(estado):
 #       estado.display()
        jogada = proxjog.fun(game, estado)
#        p = game.to_move(estado)
        estado=game.result(estado,jogada)
        lista_jogadas.append(jogada)
        proxjog = jog2 if proxjog == jog1 else jog1
    #p jogou e ganhou
    return ((jog1.nome,jog2.nome),lista_jogadas, game.utility(estado,1))

from func_timeout import func_timeout, FunctionTimedOut

def joga11com_timeout(game,jog1, jog2, nsec):
    ### jog1 e jog2 são jogadores com funções que dado um estado do jogo devolvem a jogada que escolheram
    ### devolve uma lista de jogadas e o resultado 1 se Brancas ganha -1 se Pretas ganha
    estado=game.initial
    proxjog = jog1
    lista_jogadas=[]
    while not game.terminal_test(estado):
        try:
            ReturnedValue = func_timeout(nsec, proxjog.fun, args=(game, estado))
        except FunctionTimedOut:
            print("pim!", proxjog.nome)
            ReturnedValue = None    
        jogada = ReturnedValue
        if jogada == None:
            return ((jog1.nome,jog2.nome),lista_jogadas, -1 if proxjog==jog1 else 1)
        else:
 #           p = game.to_move(estado)
            estado=game.result(estado,jogada)
            lista_jogadas.append(jogada)
            proxjog = jog2 if proxjog == jog1 else jog1
        #p jogou e ganhou
    return ((jog1.nome,jog2.nome),lista_jogadas, game.utility(estado,1))

def jogaNN(game, listaJog, listaAdv, nsec=1):
    ### devolve uma lista de tuplos da forma (j1, j2, (lista de jogadas, vencedor))
    lista_jogos=[]
    j=0
    for jog in listaJog:
        for adv in listaAdv:
            if jog != adv:
                j +=1
                lista_jogos.append(joga11com_timeout(game, jog,adv, nsec))
                print(j,jog.nome, adv.nome)
    return lista_jogos



############-----------UIUI--------------------
# máquina de jogar 11 com jogos de formulação independente. 
# gCore serve para manter as coisas fiscalizadas
##########  para ser independente dos jogos deveria devolver um método em string ou um atributo
def uiui_joga11(gameJog1, jog1, gameJog2, jog2, gCore):
    ### gameJog1 e gameJog2 são as classes com as formulações dos jogos dos respectivos jogadores 
    ### jog1 e jog2 são jogadores com funções que dado um estado do jogo devolvem a jogada que escolheram
    ### devolve uma lista de jogadas e o resultado 1 se W ganha -1 se B ganha
    estadoCore=gCore.initial
    gJog1=gameJog1()
    estadoJog1=gJog1.initial
    gJog2=gameJog2()
    estadoJog2=gJog2.initial
    proxjog = jog1
    lista_jogadas=[]
    while not gCore.terminal_test(estadoCore):
        #print('Real Board-------------------')
        #gCore.display(estadoCore)
        #gJog1.display(estadoJog1)
        #gJog2.display(estadoJog2) 
        #print('Possible actions:',gJog2.actions(estadoJog2))
        if jog1==proxjog:
            jogada = proxjog.fun(gJog1, estadoJog1)
        else:
            jogada = proxjog.fun(gJog2, estadoJog2)
        #print(jogada)
        estadoJog1=gJog1.result(estadoJog1,jogada)
        estadoJog2=gJog2.result(estadoJog2,jogada)
        estadoCore=gCore.result(estadoCore,jogada)
        lista_jogadas.append(jogada)
        proxjog = jog2 if proxjog == jog1 else jog1
    return ((jog1.nome,jog2.nome),lista_jogadas, gCore.utility(estadoCore, 1))


#############
# máquina de jogar 1x1 com jogos de formulação independente e tempo limitado
# gCore serve para manter as coisas fiscalizadas
##########  para ser independente dos jogos deveria devolver um método em string ou um atributo
def uiui_joga11com_timeout(gameJog1, jog1, gameJog2, jog2, gCore,nsec=10):
    #print('TENHO',nsec,'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
    ### jog1 e jog2 são jogadores com funções que dado um estado do jogo devolvem a jogada que escolheram
    ### devolve uma lista de jogadas e o resultado 1 se S ganha
    estadoCore=gCore.initial
    gJog1=gameJog1()
    estadoJog1=gJog1.initial
    gJog2=gameJog2()
    estadoJog2=gJog2.initial
    proxjog = jog1
    lista_jogadas=[]
    while not gCore.terminal_test(estadoCore):
        try:
            (game,estado)=(gJog1,estadoJog1) if proxjog == jog1 else (gJog2,estadoJog2)
            ReturnedValue = func_timeout(nsec, proxjog.fun, args=(game, estado))
        except FunctionTimedOut:
            print("pim!", proxjog.nome)
            ReturnedValue = None    
        jogada = ReturnedValue
        if jogada == None or jogada not in gCore.actions(estadoCore): ##verificação adicional, defensiva
            return ((jog1.nome,jog2.nome),lista_jogadas, -1 if proxjog == jog1 else 1)
        #print(jogada)
        estadoJog1=gJog1.result(estadoJog1,jogada)
        estadoJog2=gJog2.result(estadoJog2,jogada)
        estadoCore=gCore.result(estadoCore,jogada)
        lista_jogadas.append(jogada)
        proxjog = jog2 if proxjog == jog1 else jog1
    return ((jog1.nome,jog2.nome),lista_jogadas, gCore.utility(estadoCore, 1))




# -----------------  Mostra os jogos


def mostraJogo(game, logjog, verbose = False, step_by_step=False):
    (jogs,listajog,score)=logjog
    print(jogs[0],'vs',jogs[1])
    estado=game.initial
    for jog in listajog:
        if verbose:
            game.display(estado)
        if step_by_step:
            input()
        estado=game.result(estado,jog)
        if verbose:
            print()
            print("--> ", jog)
            print()
    if verbose:
        game.display(estado)
    print('Ganham as Whites' if game.utility(estado,1)==1 else 'Ganham as Blacks')


#### função para fazer campeonatos e construir a tabela final


######## Funções para jogar e fazer torneios
def faz_campeonato(jogo, listaJogadores, nsec=10):
    ### faz todos os jogos com timeout de nsec por jogada
    campeonato = jogaNN(jogo, listaJogadores, listaJogadores, nsec)
    ### ignora as jogadas e contabiliza quem ganhou
    resultado_jogos = [(a,b,n) for ((a,b),x,n) in campeonato]
    tabela = dict([(jog.nome, 0) for jog in listaJogadores])
    for jogo in resultado_jogos:
        if jogo[2] == 1:
            tabela[jogo[0]] += 1
        else:
            tabela[jogo[1]] += 1
    classificacao = list(tabela.items())
    classificacao.sort(key=lambda p: -p[1])
    print("JOGADOR", "VITÓRIAS")
    for jog in classificacao:
        print('{:11}'.format(jog[0]), '{:>4}'.format(jog[1]))



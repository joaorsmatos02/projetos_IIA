from pickle import TRUE
from elEstadoMundo import *
from searchPlus import *
import utils
from copy import deepcopy
import itertools

################################################################

estacao=(0,0)
pedonais={((4,3),(4,4))}
sentidoUnico={((3,3),(3,2)),((1,2),(2,2))}
intenso={((3,2),(3,3))}
ligeiro={}
tempos={'ligeiro': 100, 'médio': 300, 'intenso': 1000}
tempoPassageiro=10
clientes={'Lou':((1,2),(3,3)),'Gagarin':((1,2),(2,3)),'Dubenka':((1,2),(2,3))}

mundoDef=MundoBus(5,estacao,2,pedonais,sentidoUnico,intenso,ligeiro,tempos,tempoPassageiro,clientes)

class OBus(Problem):
    tabMovs={'e':(1,0),'n':(0,1),'o':(-1,0),'s':(0,-1)}
    def __init__(self, initial=None,goal=None, mundo=mundoDef):
        self.mundo=mundo
        self.initial = EstadoBus(mundo.estacao,set(mundo.clientes.keys()),set())
        self.goal=EstadoBus(mundo.estacao,set(),set())

    def move(pos,accao):
        x,y=pos
        incX,incY=OBus.tabMovs[accao]
        return ((x+incX) ,(y+incY))
    
    def actions(self, state):
        out=[]
        for a in ["e","n","o","s"]:
            x,y=state.pos
            incX,incY=OBus.tabMovs[a]
            new=((x+incX),(y+incY))
            if 0<=(x+incX)< self.mundo.dim and 0<=(y+incY)< self.mundo.dim and \
               (state.pos,new) not in self.mundo.pedonais and \
               (new,state.pos) not in self.mundo.pedonais and \
               (new,state.pos) not in self.mundo.sentidoUnico:
                out.append(a)
        ## all that should drop will drop
        droppingNum=0
        drops=set()
        for d in state.destinos:
            if self.mundo.clientes[d][1]==state.pos:
                drops.add(d)
                droppingNum+=1   

        ## the most that can be picked up will be picked up
        ## that depends on the bus capacity
        allPossiblePickups=[p for p in state.pickup if self.mundo.clientes[p][0]==state.pos]
        allPossiblePickups.sort()  # ordena

        freePlacesNum=self.mundo.capacidade-(len(state.destinos)-droppingNum)

        pickupNum=min(freePlacesNum,len(allPossiblePickups))
        if pickupNum!=0:
            acts=[(drops,set(x)) for x in (itertools.combinations(allPossiblePickups, pickupNum))]
        elif drops!=set():
            acts=[(drops,set())]
        else:
            acts = []
        return acts + out

    def result(self, estado, accao):
        if type(accao)==str:
            newPos=OBus.move(estado.pos,accao)
            return EstadoBus(newPos,estado.pickup,estado.destinos)
        else:
            drop,pickingUp=accao
            
            # dropping all people that go out of the bus here and 
            # the pickupers will be destinies
            moreDestinos=pickingUp.copy()
            newDestinos=(estado.destinos.copy() - drop).union(moreDestinos)
            
            # update pickup
            newPickup=deepcopy(estado.pickup)-pickingUp
            newPos=estado.pos

        return EstadoBus(newPos,newPickup,newDestinos)
    
    
    def path_cost(self, c, state1,action,next_state):
        if type(action)==str:
            if (state1.pos,next_state.pos) in self.mundo.ligeiro or (next_state.pos,state1.pos) in self.mundo.ligeiro:
                custo=self.mundo.tempos['ligeiro']
            elif (state1.pos,next_state.pos) in self.mundo.intenso or (next_state.pos,state1.pos) in self.mundo.intenso:
                custo=self.mundo.tempos['intenso']
            else:
                custo=self.mundo.tempos['médio']
            return c+custo
        return c+(len(action[0])+len(action[1]))*self.mundo.tempoPassageiro

#######################################################################################################################

# retorna lista com proximo local a visitar e indices dos passageiros a apanhar/largar
def maisProximo(pos, lista): 
    # [apanhar, largar]
    indices = [list(),list()]
    min = sys.maxsize # distancia a melhor posicao
    melhor = tuple() # melhor posicao a visitar atual
    for i in range(0, len(lista)):
        #verificar se a pessoa esta no autocarro ou nao
        coord = lista[i][0]
        if len(lista[i]) > 1:
            apanhar = True
        else:
            apanhar = False
        
        dist = abs(pos[0] - coord[0]) + abs(pos[1] - coord[1])
        if dist < min: # se encontar um mais proximo
            melhor = coord
            min = dist # novo minimo
            indices[0] = list() # reiniciar lista
            indices[1] = list()
            if not apanhar:
                indices[0].append(i)
            else:
                indices[1].append(i)
        elif min == dist:
            if melhor == coord:
                if not apanhar:
                    indices[0].append(i)
                else:
                    indices[1].append(i)
            else:
                if coord[0] < melhor[0] or (coord[0] == melhor[0] and coord[1] < melhor[1]):
                    melhor = coord
                    min = dist # novo minimo
                    indices[0] = list() # reiniciar lista
                    indices[1] = list()
                    if not apanhar:
                        indices[0].append(i)
                    else:
                        indices[1].append(i)

        
    return [melhor,indices]

def planoImpaciente(mundo):
    # custo e rota totais
    custo = 0
    rota = list()

    # obter todos os nomes e pontos a visitar
    clientes = list(mundo.clientes.keys())
    pontos = list(mundo.clientes.values())

    if len(clientes) == 0:
        return ([],0)

    # posicao atual do autocarro
    pos = mundo.estacao

    # apanhar/largar clientes
    while len(clientes) != 0: # enquanto houver clientes a apanhar ou largar

        proximo = maisProximo(pos, pontos) # indices do clientes a apanhar a seguir
        
        for i in range(0,len(proximo[1][1])):
            # atualizar listas de pontos e clientes
            pontos[proximo[1][1][i]]= list(pontos[proximo[1][1][i]])
            del pontos[proximo[1][1][i]][0]
            pontos[proximo[1][1][i]] = tuple(pontos[proximo[1][1][i]])

            # converter indices em nomes
            proximo[1][1][i] = clientes[proximo[1][1][i]]

        for i in reversed(range(0,len(proximo[1][0]))): 
            # converter indices para nomes
            cli = clientes[proximo[1][0][i]]

            # atualizar listas de pontos e clientes
            del clientes[proximo[1][0][i]]
            del pontos[proximo[1][0][i]]

            proximo[1][0][i] = cli
            
        proximo[1][0] = sorted(proximo[1][0])
        proximo[1][1] = sorted(proximo[1][1])
        proximo[1] = tuple(proximo[1])

        novoMundo = deepcopy(mundo)
        novoMundo = novoMundo._replace(estacao = pos)
        novoMundo = novoMundo._replace(clientes=dict())

        # adicionar a rota e custo
        b = OBus(mundo=novoMundo)
        b.goal = EstadoBus(proximo[0], set(), set())

        caminho = uniform_cost_search(b) # planear rota entre pos atual e pos do cliente
        rota.extend(caminho.solution()) # adicionar movimentos
        rota.append(proximo[1]) # adicionar entradas/saidas
        custo += caminho.path_cost
        custo += mundo.tempoPassageiro * (len(proximo[1][0]) + len(proximo[1][1])) # adicionar tempo dos passageiros

        pos = proximo[0] # atualizar posicao atual

    b.initial = b.goal
    b.goal = b.goal._replace(pos=mundo.estacao)
    volta = uniform_cost_search(b) # planear rota de volta a estacao
    rota.extend(volta.solution())
    custo += volta.path_cost

    return (rota, custo)

########################################################################################################

	
# Mundo 1, em que vamos apanhar um sujeito e largá-lo logo a seguir e regressar

dimensao=7
estacao=(1,1)
capacidade=2
pedonais={((2,2),(2,3)),((2,2),(3,2)),((1,2),(2,2)),((2,1),(2,2))}
sentidoUnico={((5,1),(5,0)),((4,0),(5,0)),((3,0),(2,0))}
intenso={((0,0),(1,0)),((1,0),(2,0))}
ligeiro={((2,3),(2,4))}
tempos={'ligeiro': 200, 'médio': 500, 'intenso': 2000}
tempoPassageiro=10
clientes={'A':((2,1),(2,1)), 'B':((0,1),(0,1))}
mundo1=MundoBus(dimensao,estacao,capacidade,pedonais,sentidoUnico,intenso,ligeiro,tempos,tempoPassageiro,clientes)

print(planoImpaciente(mundo1))
from elEstadoMundo import *
from searchPlus import *
from itertools import combinations
import copy

# Mundo por defeito
estacao=(0,0)
pedonais={((4,3),(4,4))}
sentidoUnico={((3,3),(3,2)),((1,2),(2,2))}
intenso={((3,2),(3,3))}
ligeiro={((2,1),(2,2))}
tempos={'ligeiro': 100, 'médio': 300, 'intenso': 1000}
tempoPassageiro=10
clientes={1:((1,2),(3,3)),2:((1,2),(2,3))}

mundoDef=MundoBus(5,estacao,2,pedonais,sentidoUnico,intenso,ligeiro,tempos,tempoPassageiro,clientes)

class OBus(Problem):
    
    def __init__(self, initial=None,goal=None, mundo=mundoDef):
        if initial == None:
            initial = EstadoBus(pos=mundo.estacao, pickup=set(mundo.clientes.keys()), destinos=set()) # inicial default
        self.initial = initial

        if goal == None:
            goal = EstadoBus(pos=mundo.estacao, pickup=set(), destinos=set()) # goal default
        self.goal = goal

        self.mundo = mundo
    
    def actions(self, state):
        # verificar quem pode sair
        e = state.destinos
        exit = set()
        for p in e:
            if self.mundo.clientes.get(p)[1] == state.pos:
                exit.add(p)

        # verificar quem pode entrar
        passengers = state.pickup
        passengersHere = list()
        for p in passengers:
            if self.mundo.clientes.get(p)[0] == state.pos:
                passengersHere.append(p)

        # verificar combinacoes aceitaveis
        capacity = self.mundo.capacidade - len(state.destinos) + len(exit) # calcular quantos passageiros podem entrar depois das saidas
        if capacity != 0 and (len(exit) != 0 or len(passengersHere) != 0):
            enter = list(combinations(sorted(passengersHere), min(capacity,len(passengersHere))))
            for i in range(0,len(enter)):
                enter[i] = set(enter[i])
            out = [(exit, enter[i]) for i in range(0, len(enter))]
        else:
            out = list()

        #verificar movimentos possiveis
        size = self.mundo.dim
        position = state.pos

        # verificar se nao esta na ponta, se nao e pedonal e se cumpre sentido unico
        n = position[1] < size - 1 and \
            (position, (position[0], position[1] + 1)) not in self.mundo.pedonais and \
            ((position[0], position[1] + 1), position) not in self.mundo.sentidoUnico

        s = position[1] != 0 and \
            ((position[0], position[1] - 1), position) not in self.mundo.pedonais and \
            ((position[0], position[1] - 1), position) not in self.mundo.sentidoUnico

        e = position[0] < size - 1 and \
            (position, (position[0] + 1, position[1])) not in self.mundo.pedonais and \
            ((position[0] + 1, position[1]), position) not in self.mundo.sentidoUnico

        o = position[0] != 0 and \
            ((position[0] - 1, position[1]), position) not in self.mundo.pedonais and \
            ((position[0] - 1, position[1]), position) not in self.mundo.sentidoUnico

        if e:
            out.append('e')
        if n:
            out.append('n')
        if o:
            out.append('o')
        if s:
            out.append('s')

        return out

    def result(self, estado, accao):
        result = copy.deepcopy(estado) # copiar estado

        # se sairem ou entrarem passageiros
        if type(accao) == tuple:
            for p in accao[0]:
                result.destinos.remove(p)
            for p in accao[1]:
                result.pickup.remove(p)
                result.destinos.add(p)

        # se o autocarro andar
        else: 
            temp = list(result.pos)
            if accao == 'n':
                temp[1] += 1
            elif accao == 's':
                temp[1] -= 1
            elif accao == 'e':
                temp[0] += 1
            else:
                temp[0] -= 1
            result = result._replace(pos=tuple(temp))

        return result

    def path_cost(self, c, state1, action, state2):
        # verificar se sairam/entraram passageiros
        if type(action) == tuple:
            c += self.mundo.tempoPassageiro * (len(action[0]) + len(action[1]))

        # verificar se andou
        else:
            if action == 'n' or action == 'e': # se andou para norte ou este
                path = (state1.pos, state2.pos)
            else: # se andou para sul ou oeste
                path = (state2.pos, state1.pos)

            # verificar estado do transito no caminho
            if path in self.mundo.ligeiro:
                c += self.mundo.tempos.get("ligeiro")
            elif path in self.mundo.intenso:
                c += self.mundo.tempos.get("intenso")
            else:
                c += self.mundo.tempos.get("médio")
            
        return c

###########################################

dimensao=7
estacao=(1,1)
capacidade=2
pedonais={((2,2),(2,3)),((2,2),(3,2)),((1,2),(2,2)),((2,1),(2,2))}
sentidoUnico={((0,0),(0,1)),((1,0),(0,0)),((5,1),(5,0)),((4,0),(5,0))}
intenso={((1,2),(1,3))}
ligeiro={((2,3),(2,4))}
tempos={'ligeiro': 200, 'médio': 500, 'intenso': 1500}
tempoPassageiro=10
clientes={85:((2,2),(2,5)),115:((2,2),(5,5)),111:((2,2),(3,3)),5:((2,2),(2,5)),15:((2,2),(5,5)),11:((2,2),(3,3)),8:((2,4),(2,2))}
mundo1=MundoBus(dimensao,estacao,capacidade,pedonais,sentidoUnico,intenso,ligeiro,tempos,tempoPassageiro,clientes)

xx=OBus(mundo=mundo1)

actions=[xx.actions(est) for est in [EstadoBus(pos,{15,5,11},{8}) for pos in [(1,2),(0,5),(1,4),(4,2),(0,0),(2,2),(1,1)]]]
print(actions)
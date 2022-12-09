from collections import namedtuple

MundoBus = namedtuple('MundoBus',['dim','estacao','capacidade','pedonais','sentidoUnico','intenso','ligeiro','tempos','tempoPassageiro','clientes'])


# impressão del mundo mais pretty

def pretty_mundo(mundo):
    print('-'*50)
    print('Dimensão do mundo:',mundo.dim)
    print('Estação:',mundo.estacao)
    print('Capacidade do autocarro:',mundo.capacidade)
    print('As ruas pedonais:')
    for p in mundo.pedonais:
        print(' '*5,p)
    print('As ruas de um só sentido:')
    for p in mundo.sentidoUnico:
        print(' '*5,p)
    print('As ruas com tráfego ligeiro:')
    for p in mundo.ligeiro:
        print(' '*5,p)
    print('As ruas com tráfego intenso:')
    for p in mundo.intenso:
        print(' '*5,p)
    print('Tempo médio a atravessar as ruas de:')
    for p in mundo.tempos:
        print(' '*5,p,':',str(mundo.tempos[p])+'s')
    print('Tempo médio para um passageiro sair ou entrar no Bus:',str(mundo.tempoPassageiro)+'s')
    print('Clientes:')
    for p in mundo.clientes:
        print(' '*5,p,"-",mundo.clientes[p])
    print('-'*60)


# ---------- Implementacao do Estado

TheBus = namedtuple('Bus',['pos', 'pickup','destinos'])

class EstadoBus(TheBus):
    def __hash__(self):
        new=()
        for x in self:
            new=new+(str(x),)
        return hash(new)
    
    def strCoderunner(self):
        return 'EstadoBus('+ str(self[0]) +','+ \
                             str(sorted(self[1]))+','+ \
                             str(sorted(self[2]))+')'
    
    def prettyPrint(self):
        tabs=5
        out="Bus:\n"
        out+=" "*tabs+"Local:"+str(self.pos)+'\n'
        out+=' '*tabs+"Largar: "+str(self.destinos)+"\n"
        out+=' '*tabs+"Apanhar: "+str(self.pickup)+'\n' 
        print(out)
        
def printListaEstados(L):
    print('[',end='')
    for e in L:
        print(e.strCoderunner(),'',end='')
    print(']')
    
def minPlus(l):
    if l:
        return min(l)
    return 0

from math import log2

def transformaPontos(pontos, intervalos):
    for p in pontos.keys():
        novoTuplo = []
        for t in range(0,len(pontos[p]) - 1):
            intervalo = intervalos[t]
            for i in range(0,len(intervalo) + 1):
                if i == 0:
                    if pontos[p][t] < intervalo[i]:
                        novoTuplo.append(1)
                        break
                elif i == len(intervalo):
                    novoTuplo.append(len(intervalo) + 1)
                    break
                elif pontos[p][t] < intervalo[i] and pontos[p][t] > intervalo[i-1]:
                    novoTuplo.append(i + 1)
                    break
        novoTuplo.append(pontos[p][-1])
        pontos[p] = tuple(novoTuplo)
    return pontos



def escolheAtributo(pontos, indices, dominios, classes, pedadogico=False):
    medias = []
    dicionarios = []
    for i in indices: # para cada atributo
        if pedadogico:
            print("---> Vamos verificar o atributo com índice: " + str(i))
        
        # filtrar por cada valor possivel
        distribuicao = []
        dicionariosIndice = []
        for v in dominios[i]: 
            if pedadogico:
                print("filtro os dados para o atributo " + str(i) + " = " + str(v))
            dicionario = {p: d for p, d in pontos.items() if d[i] == v}
            dicionariosIndice.append(dicionario)
            if pedadogico:
                print(str(dicionario))
            dist = []
            for c in classes: # calcular distribuicao dos pontos pelas classes
                dist.append(len({p: d for p, d in dicionario.items() if d[-1] == c}))
            distribuicao.append(dist)
        dicionarios.append(dicionariosIndice)

        # calcular entropia
        if pedadogico:
            print("Distribuição dos pontos pelas classes: " + str(distribuicao))
        entropias = []
        for d in distribuicao: 
            total = 0
            if pedadogico:
                print("entropia(" + str(d) + ")=", end="")
            for num in d:
                if num != 0:
                    total += -(num/sum(d)) * log2(num/sum(d))
                if pedadogico:
                    print("-" + str(num) + "/" + str(sum(d)) + ".log2(" + str(num) + "/" + str(sum(d)) + ")", end="")
            if pedadogico:
                print("=" + str(round(total, 4)))
            entropias.append(round(total, 4))

        # calcular entropia media
        if pedadogico:
            print("entropiaMédia(" + str(distribuicao) + ")=", end="") 
        media = 0
        for d in range(0,len(distribuicao)):
            media += sum(distribuicao[d])/len(pontos)*entropias[d]
            if pedadogico:
                print(str(sum(distribuicao[d])) + "/" + str(len(pontos)) + "x" + str(entropias[d]), end="")
                if d != len(distribuicao) - 1:
                    print("+", end="")
        media = round(media,4)
        medias.append(media)
        if pedadogico:
            print("=" + str(media))

    # construir tuplo final
    atributoMedia = list(zip(indices,medias))
    melhor = min(atributoMedia, key=lambda tup: tup[1])
    lista = dicionarios[melhor[0]]
    
    return (atributoMedia,melhor,lista)

pontos = {1:(0.5,3.5,'quadrado'), 2:(0.5,6.5,'bola'), 3:(1.5,5.5,'quadrado'),
        4:(1.5,8.5,'bola'),5:(2.5,1.5,'quadrado'), 6:(2.5,3.5,'quadrado'),
        7:(3.5,4.5,'quadrado'), 8:(4.5,0.5,'quadrado'),9:(4.5,2.5,'quadrado'),
        10:(4.5,7.5,'bola'), 11:(6.5,1.5,'quadrado'), 12:(7.5,1.5,'x'),
        13:(7.5,3.5,'x'), 14:(7.5,5.5,'bola'), 15:(7.5,8.5,'bola'),
        16:(8.5,2.5,'x'),17:(8.5,4.5,'bola')}
intervalos = {0:[2,4,6,8],1:[2,4,6,8]}
classes = ['quadrado','bola','x']
atributos = ['X','Y']
data = transformaPontos(pontos,intervalos)
output = escolheAtributo(data,[0,1],[[1,2,3,4,5]]*2,classes,True)
print(output)
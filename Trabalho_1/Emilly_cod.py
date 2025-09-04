import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import random
import math
import sys
import numpy as np
from matplotlib.patches import Arc

# Parametros 
TAMANHO_DO_PLANO = 10000
QUANT_OBSTACULOS = 10
RAIO = 600

PONTO_INICIO = (0,0)
PONTO_FIM = (TAMANHO_DO_PLANO,TAMANHO_DO_PLANO)

# lista com as cordenadas de onde estão os obstaculos 
mapa_obstaculos = []

def encerrar_com_mensagem(mensagem, cor=None, finalizar=True, sem_espaço=None):
    
    if sem_espaço == 1: 
        mensagem = 'Não foi possível adicionar todos os obstáculos'
        cor = 'red'
        fontweight = 'bold'
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    else:
        if cor is None:
            cor = 'green'
        fontweight = 'bold'

    ax.text(0.5, 0.5, mensagem, ha='center', va='center', 
            fontsize=16, color=cor, fontweight=fontweight, transform=ax.transAxes)
    plt.draw()

    if finalizar:
        plt.show(block=True)
        sys.exit()

def calcular_distancia(ponto1, ponto2): 
    return math.sqrt((ponto1[0] - ponto2[0])**2 + (ponto1[1] - ponto2[1])**2) #  é a formula Euclidiana basicamente,  melhor forma pelo que eu vi ( a outra que eu tenti ainda tinha sobreposição na diagonal )

def verifica_intervalo(ponto_inserido,ponto_verifica):
    distancia = calcular_distancia(ponto_inserido,ponto_verifica)
    return ((distancia > (RAIO * 2)) | (distancia < 0))

def calcular_laterais(ponto_centro):
    ponto_cima = (ponto_centro[0] + RAIO,ponto_centro[1])
    ponto_baixo = (ponto_centro[0] - RAIO,ponto_centro[1])
    ponto_direito = (ponto_centro[0] ,ponto_centro[1] + RAIO)
    ponto_esquerdo = (ponto_centro[0] ,ponto_centro[1] - RAIO)
    return  ponto_cima,ponto_baixo,ponto_direito,ponto_esquerdo

def segmento_entra_no_circulo(A, B, centro, raio, eps=1e-9, permitir_tangencia=True):

    # Retorna True se o INTERIOR do segmento AB entra no INTERIOR do círculo (centro, raio).
    # Exclui exatamente os endpoints (t=0 e t=1) para não bloquear arestas por tocar na borda no ponto de origem.
 
    (x1, y1), (x2, y2) = A, B
    (h, k) = centro
    dx = x2 - x1
    dy = y2 - y1

    AB2 = dx*dx + dy*dy
    if AB2 == 0:
        # segmento degenerado
        d = calcular_distancia(A, (h, k))
        return d < (raio - eps)

    # parametro t do ponto do segmento mais próximo do centro do círculo
    t = ((h - x1)*dx + (k - y1)*dy) / AB2

    # considera apenas o INTERIOR do segmento
    if t <= eps or t >= 1 - eps:
        return False

    # Ponto projetado no interior
    proj = (x1 + t*dx, y1 + t*dy)
    d = calcular_distancia(proj, (h, k))

    if permitir_tangencia:
        # invalida só se o interior entrar mesmo (distância menor que o raio)
        return d < (raio - eps)
    else:
       
        return d <= (raio + eps)

def colisao_com_obstaculos_interior(A, B, mapa):
    """True se o interior do segmento AB entra no interior de QUALQUER circulo do mapa."""
    for centro, _ in mapa:
        if segmento_entra_no_circulo(A, B, centro, RAIO):
            return True
    return False

def encontrar_possibilidades(dict_caminhos, ponto_inicial, ponto_final):
    """Busca DFS iterativa para encontrar caminho do ponto inicial ao final."""
    stack = [(ponto_inicial, [ponto_inicial])]
    visited = set()
    
    while stack:
        current, path = stack.pop()
        
        if current in visited:
            continue
        visited.add(current)
        
        if current == ponto_final:
            return path
            
        # Adiciona vizinhos à pilha
        for neighbor in dict_caminhos.get(current, []):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    
    return None

def ponto_mesmo_centroid(ponto1, ponto2, centroids, raio_size):
    """Verifica se ambos os pontos pertencem ao mesmo centróide."""
    centroid_ponto1 = None
    centroid_ponto2 = None
    eps = 1e-6

    # procura centróide para ponto1
    for i, centroid in enumerate(centroids):
        if calcular_distancia(ponto1, centroid) <= raio_size + eps:
            centroid_ponto1 = i
            break

    # procura centróide para ponto2
    for i, centroid in enumerate(centroids):
        if calcular_distancia(ponto2, centroid) <= raio_size + eps:
            centroid_ponto2 = i
            break

    # se ambos pertencem ao mesmo centróide (mesmo índice), retorna True
    if centroid_ponto1 is not None and centroid_ponto2 is not None and centroid_ponto1 == centroid_ponto2:
        return True, centroids[centroid_ponto1], centroid_ponto1

    return False, None, None

#criação dos obstaculos 
# - cada obstaculo é um circulo de raio fixo (já defini la em cima )
# - cada circulo é composto por apenas 4 pontos ( cima baixo esquerda direita) criar função para culcular a localização dos pontos baseado no raio 
# - os obstaculos não devem ter nenhuma sobreposição 
# - eles não podem se encostar então nas verificação é sempre maior que o raio( quando botei igual ou maior ele podem gerar obstaculso com um ponto encostado )

if __name__ == "__main__":
    sem_espaço = 0
    # plotando o fundo(lembra de que um obstaculo tbm não deve sobrepor esse pontos)
    fig, ax = plt.subplots()
    ax.set_xlim(0, TAMANHO_DO_PLANO)
    ax.set_ylim(0, TAMANHO_DO_PLANO)
    ax.set_aspect('equal')
    # ax.set_facecolor("black")  

    # plano cartesiano (as retas do eixo)
    ax.grid(color='gray', linestyle='--', alpha=0.3)
    ax.axhline(0, color='white', linewidth=0.5)
    ax.axvline(0, color='white', linewidth=0.5)

    # o pontos inicial e final são fixos (um obstaculo não deve sobrepor esse pontos)
    ax.plot(PONTO_INICIO[0],PONTO_INICIO[1], 'go', markersize=10, label='Início')
    ax.plot(PONTO_FIM[0],PONTO_FIM[1], 'ro', markersize=10, label='Fim')

    cores_planetas = ['blue', 'orange', 'cyan', 'magenta', 'red', 'green']

    for i in range(QUANT_OBSTACULOS):
        tentativas = 0
        while True:
            tentativas += 1

            if tentativas >= 1000:
                sem_espaço = 1
                break  

            x = random.uniform(RAIO, TAMANHO_DO_PLANO - RAIO)
            y = random.uniform(RAIO, TAMANHO_DO_PLANO - RAIO)
            novo_centro = (x, y)
            
            if calcular_distancia(novo_centro, PONTO_INICIO) < RAIO: 
                continue 
            if calcular_distancia(novo_centro, PONTO_FIM) < RAIO: 
                continue 
            if any(not verifica_intervalo(novo_centro, obstaculo[0]) for obstaculo in mapa_obstaculos): 
                continue
            
            mapa_obstaculos.append((novo_centro,calcular_laterais(novo_centro)))
            break
        
        for obstaculo in mapa_obstaculos:
            # cor_planeta = random.choice(cores_planetas)
            # circulo = plt.Circle(obstaculo[0], RAIO, color=cor_planeta, alpha=0.7)
            circulo = plt.Circle(obstaculo[0], RAIO, color="gray", alpha=0.7)
            
            for ponto in obstaculo[1]:
                ax.plot(ponto[0],ponto[1], 'o', markersize=2, color="black")
                
            ax.add_patch(circulo)
            # plt.pause(0.10)  
    
    print(mapa_obstaculos)

    todos_pontos = []
    pontos_circulo_idx = []  # para saber de qual círculo é cada ponto
    for idx, (centro, pontos) in enumerate(mapa_obstaculos):
        for p in pontos:
            todos_pontos.append(p)
            pontos_circulo_idx.append(idx)

    todos_pontos.append(PONTO_INICIO)
    pontos_circulo_idx.append(-1)  # índice especial só pra marcar que não é de círculo
    todos_pontos.append(PONTO_FIM)
    pontos_circulo_idx.append(-1)

    # Coletar todas as arestas válidas e desenhá-las (linhas finas azuis)
    retas = []
    arestas_qtd = 0
    for i in range(len(todos_pontos)):
        for j in range(i+1, len(todos_pontos)):
            # não conectar pontos do MESMO círculo (cortaria o interior do próprio círculo)
            if pontos_circulo_idx[i] == pontos_circulo_idx[j]:
                continue

            p1, p2 = todos_pontos[i], todos_pontos[j]

            # invalida se o INTERIOR do segmento entrar no interior de qualquer círculo
            if colisao_com_obstaculos_interior(p1, p2, mapa_obstaculos):
                continue

            # se chegou aqui, é uma aresta válida
            retas.append((p1, p2))
            # desenha cada aresta válida em azul fino
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='blue', linewidth=0.5, alpha=0.6)
            arestas_qtd += 1

    print(f"Arestas válidas encontradas: {arestas_qtd}")

    # Adicionar também as arestas internas ligando laterais de cada obstáculo (diagonais)
    # posicoes_centroides: lista de tuples (cima, baixo, direito, esquerdo)
    posicoes_centroides = [obst[1] for obst in mapa_obstaculos]
    for (cima, baixo, direito, esquerdo) in posicoes_centroides:
        # ligações diagonais dentro do mesmo círculo (não cruzam interior porque são na borda)
        retas.append((cima, esquerdo))
        retas.append((cima, direito))
        retas.append((baixo, esquerdo))
        retas.append((baixo, direito))

    # Construir grafo de conectividade bidirecionalmente
    dict_caminhos = {}

    # Inicializa todos os pontos no dicionário
    for obstaculo in mapa_obstaculos:
        for ponto_lateral in obstaculo[1]:
            dict_caminhos[ponto_lateral] = []
    dict_caminhos[PONTO_INICIO] = []
    dict_caminhos[PONTO_FIM] = []

    # Adiciona todas as arestas válidas (incluindo as internas dos obstáculos)
    for aresta in retas:
        ponto_a, ponto_b = aresta[0], aresta[1]
        # Adiciona conexão bidirecional
        if ponto_a in dict_caminhos and ponto_b in dict_caminhos:
            dict_caminhos[ponto_a].append(ponto_b)
            dict_caminhos[ponto_b].append(ponto_a)



    for key, value in dict_caminhos.items():
        print(f"Reta: {key}, Pontos: {value}")

    # Buscar caminho do início ao fim
    ponto_inicial = PONTO_INICIO
    ponto_final = PONTO_FIM

    caminho_encontrado = encontrar_possibilidades(dict_caminhos, ponto_inicial, ponto_final)
    
    if caminho_encontrado:
        print(f"Caminho encontrado com {len(caminho_encontrado)} pontos!")
        print("Caminho:", caminho_encontrado)
        
        # Lista dos centros dos obstáculos para verificar se pontos pertencem ao mesmo obstáculo
        centroids = [centro for centro, _ in mapa_obstaculos]
        raio_size = RAIO
        
        # Desenhar o caminho encontrado
        for i in range(len(caminho_encontrado) - 1):
            ponto1 = caminho_encontrado[i]
            ponto2 = caminho_encontrado[i + 1]

            mesmo_centro, centroid, _ = ponto_mesmo_centroid(ponto1, ponto2, centroids, raio_size)
            if mesmo_centro:
                # Desenhar arco ao redor do obstáculo: escolher o arco MAIS CURTO entre angulos
                angulo1 = np.degrees(np.arctan2(ponto1[1] - centroid[1], ponto1[0] - centroid[0]))
                angulo2 = np.degrees(np.arctan2(ponto2[1] - centroid[1], ponto2[0] - centroid[0]))

                # Normaliza para [0,360)
                a1 = angulo1 % 360
                a2 = angulo2 % 360

                # Diferença no sentido CCW de a1->a2
                diff = (a2 - a1) % 360

                # Se diff <= 180, o arco CCW de a1 até a2 é o menor; caso contrário, invertemos
                if diff <= 180:
                    theta1, theta2 = a1, a2
                else:
                    theta1, theta2 = a2, a1

                arco = Arc(centroid, width=2*raio_size, height=2*raio_size,
                          theta1=theta1, theta2=theta2, color="green", linewidth=3, zorder=5)
                ax.add_patch(arco)
            else:
                # Desenhar linha reta entre obstáculos
                ax.plot([ponto1[0], ponto2[0]], [ponto1[1], ponto2[1]], 
                       color='red', linewidth=3, label='Caminho' if i == 0 else "")
        
        # Destacar pontos do caminho
        for ponto in caminho_encontrado:
            ax.plot(ponto[0], ponto[1], 'yo', markersize=6, markeredgecolor='black', markeredgewidth=1)
        
        ax.legend()
        encerrar_com_mensagem("Caminho encontrado!", cor='lime', sem_espaço=sem_espaço)
    else:
        print("Nenhum caminho encontrado!")
        encerrar_com_mensagem("Nenhum caminho encontrado!", cor='red', sem_espaço=sem_espaço)

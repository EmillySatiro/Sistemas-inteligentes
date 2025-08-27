import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import random
import math
import sys

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
    # True se o interior do segmento AB entra no interior de QUALQUER circulo do mapa.
    for centro, _ in mapa:
        if segmento_entra_no_circulo(A, B, centro, RAIO):
            return True
    return False

#criação dos obstaculos 
# - cada obstaculo é um circulo de raio fixo (já defini la em cima )
# - cada circulo é composto por apenas 4 pontos ( cima baixo esquerda direita) criar função para culcular a localização dos pontos baseado no raio 
# - os obstaculos não devem ter nenhuma sobreposição 
# - eles não podem se encostar então nas verificação é sempre maior que o raio( quando botei igual ou maior ele podem gerar obstaculso com um ponto encostado )

if __name__ == "__main__":
    sem_espaço = 0
    # plotando o fundo(lembra de que um obstaculo tbm não deve fica em partes fora da borda ou seja tenho que gerar inteiro dentro das bordas)
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
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-', linewidth=0.5)
            arestas_qtd += 1

    print(f"Arestas válidas desenhadas: {arestas_qtd}")

    encerrar_com_mensagem("Todos os planetas foram posicionados!", cor='lime', sem_espaço=sem_espaço)

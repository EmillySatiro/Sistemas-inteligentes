import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import random
import math
import sys

# Parametros 
TAMANHO_DO_PLANO = 10000
QUANT_OBSTACULOS = 50
RAIO = 600

PONTO_INICIO = (0,0)
PONTO_FIM = (TAMANHO_DO_PLANO,TAMANHO_DO_PLANO)

# lista com as cordenadas de onde estão os obstaculos 
mapa_obstaculos = []

def encerrar_com_mensagem(mensagem, cor='red'):
    ax.text(0.5, 0.5, mensagem, ha='center', va='center', fontsize=16, color=cor, transform=ax.transAxes)
    plt.draw()
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

#criação dos obstaculos 
# - cada obstaculo é um circulo de raio fixo (já defini la em cima )
# - cada circulo é composto por apenas 4 pontos ( cima baixo esquerda direita) criar função para culcular a localização dos pontos baseado no raio 
# - os obstaculos não devem ter nenhuma sobreposição 
# - eles não podem se encostar então nas verificação é sempre maior que o raio( quando botei igual ou maior ele podem gerar obstaculso com um ponto encostado )
if __name__ == "__main__":
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
                encerrar_com_mensagem("Não há mais espaço!", cor='red')

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
            # plt.pause(0.25)  
    
    print(mapa_obstaculos)
    
    encerrar_com_mensagem("Todos os planetas foram posicionados!", cor='lime')

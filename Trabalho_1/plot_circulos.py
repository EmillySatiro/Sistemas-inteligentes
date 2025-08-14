import random
import math
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

MIN = 0
MAX = 1000

PONTO_INI = (MIN,MIN)
PONTO_FIM = (MAX,MAX)

QTD_OBSTACULO = 50
RAIO_OBSTACULO = 25

pontos_usados = [PONTO_INI,PONTO_FIM]
pontos_nao_pode = [PONTO_INI,PONTO_FIM]

def distancia_circulo(ponto_inserido,ponto_verifica):
    return math.sqrt(math.pow(ponto_inserido[0] - ponto_verifica[0],2) + math.pow(ponto_inserido[1] - ponto_verifica[1],2))

def verifica_intervalo(ponto_inserido,ponto_verifica):
    distancia = distancia_circulo(ponto_inserido,ponto_verifica)
    return ((distancia > (RAIO_OBSTACULO * 2)) | (distancia < 0))

def rand_num():
    return (random.randint(MIN + RAIO_OBSTACULO,MAX - RAIO_OBSTACULO))

def gerar_posicao():
    i = 0
    
    while i < QTD_OBSTACULO:
        pode = True
        ponto_gerado = (rand_num(),rand_num())

        for ponto_atual in pontos_usados:
            if not (verifica_intervalo(ponto_gerado,ponto_atual) & (ponto_gerado not in pontos_nao_pode)):
                pode  = False
        
        if pode:
            pontos_usados.append(ponto_gerado)
            i += 1
        else:
            pontos_nao_pode.append(ponto_gerado)
            
def plotar_grafico():
    
    for ponto in pontos_usados[2:]:
        circulo = plt.Circle(ponto, RAIO_OBSTACULO, color='gray', alpha=0.5)
        ax.add_patch(circulo)
        ax.plot(ponto[0], ponto[1], 'ko', markersize=3)

    ax.plot(PONTO_INI[0], PONTO_INI[1], 'go', markersize=10, label='Início')

    ax.plot(PONTO_FIM[0], PONTO_FIM[1], 'ro', markersize=10, label='Fim')

    ax.set_xlim(MIN, MAX)
    ax.set_ylim(MIN, MAX)
    
    ax.set_aspect('equal')
    ax.legend()
    plt.title('Obstáculos, Início e Fim')
    plt.show()

if __name__ == '__main__':
    gerar_posicao()
    print(pontos_usados)
    print(len(pontos_usados))
    plotar_grafico()
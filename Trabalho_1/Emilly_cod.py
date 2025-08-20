import matplotlib.pyplot as plt
import random
import math
import sys

# Parametros 
Tamanho_do_plano = 10000
raio = 600
ponto_inico = (0,0)
ponto_fim = (Tamanho_do_plano,Tamanho_do_plano)

def calcular_distancia(ponto1, ponto2): 
    return math.sqrt((ponto1[0] - ponto2[0])**2 + (ponto1[1] - ponto2[1])**2) #  é a formula Euclidiana basicamente,  melhor forma pelo que eu vi ( a outra que eu tenti ainda tinha sobreposição na diagonal )

quant_obstaculos = int(input("Digite a quantidade de obstáculos: "))

# lista com as cordenadas de onde estão os obstaculos 
mapa_obstaculos = []

# plotando o fundo(lembra de que um obstaculo tbm não deve fica em partes fora da borda ou seja tenho que gerar inteiro dentro das bordas)
fig, ax = plt.subplots()
ax.set_xlim(0, Tamanho_do_plano)
ax.set_ylim(0, Tamanho_do_plano)
ax.set_aspect('equal')
ax.set_facecolor("black")  


# plano cartesiano (as retas do eixo)
ax.grid(color='gray', linestyle='--', alpha=0.3)
ax.axhline(0, color='white', linewidth=0.5)
ax.axvline(0, color='white', linewidth=0.5)

# estrelas no fundo
num_estrelas = 500
estrelas_x = [random.uniform(0, Tamanho_do_plano) for _ in range(num_estrelas)]
estrelas_y = [random.uniform(0, Tamanho_do_plano) for _ in range(num_estrelas)]
ax.scatter(estrelas_x, estrelas_y, s=2, color='white', alpha=0.8)


# o pontos inicial e final são fixos (um obstaculo não deve sobrepor esse pontos)
ax.plot(ponto_inico[0], ponto_inico[1], 'go', markersize=10, label='Início')
ax.plot(ponto_fim[0], ponto_fim[1], 'ro', markersize=10, label='Fim')

cores_planetas = ['blue', 'orange', 'cyan', 'magenta', 'red', 'green']

def encerrar_com_mensagem(mensagem, cor='red'):
    ax.text(0.5, 0.5, mensagem, ha='center', va='center', fontsize=16, color=cor, transform=ax.transAxes)
    plt.draw()
    plt.show(block=True)
    sys.exit()

#criação dos obstaculos 
# - cada obstaculo é um circulo de raio fixo (já defini la em cima )
# - cada circulo é composto por apenas 4 pontos ( cima baixo esquerda direita) criar função para culcular a localização dos pontos baseado no raio 
# - os obstaculos não devem ter nenhuma sobreposição 
# - eles não podem se encostar então nas verificação é sempre maior que o raio( quando botei igual ou maior ele podem gerar obstaculso com um ponto encostado )

for i in range(quant_obstaculos):
    tentativas = 0
    while True:
        tentativas += 1

        if tentativas >= 1000:
            encerrar_com_mensagem("Não há mais espaço!", cor='red')

        x = random.uniform(raio, Tamanho_do_plano - raio)
        y = random.uniform(raio, Tamanho_do_plano - raio)
        novo_centro = (x, y)
        
        if calcular_distancia(novo_centro, ponto_inico) < raio: 
            continue 
        if calcular_distancia(novo_centro, ponto_fim) < raio: 
            continue 
        if any(calcular_distancia(novo_centro, obstaculo) < (2*raio + 1) for obstaculo in mapa_obstaculos): 
            continue
        
        mapa_obstaculos.append(novo_centro)
        break

    cor_planeta = random.choice(cores_planetas)
    circulo = plt.Circle(novo_centro, raio, color=cor_planeta, alpha=0.7)
    ax.add_patch(circulo)
    plt.pause(0.25)  

encerrar_com_mensagem("Todos os planetas foram posicionados!", cor='lime')

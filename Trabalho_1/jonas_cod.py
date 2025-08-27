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

mapa_obstaculos = []
arestas_globais = []

def encerrar_com_mensagem(ax,mensagem, cor='red'):
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

def calcular_distancia_reta(r_a, r_b, r_c, c_x, c_y):
    cima = abs((r_a * c_x) + (r_b * c_y) + r_c)
    baixo = math.sqrt((r_a ** 2) + (r_b ** 2))
    return cima / baixo


def gerar_obstaculo_existente(novo_centro):
    if calcular_distancia(novo_centro, PONTO_INICIO) < RAIO:
        return True
    if calcular_distancia(novo_centro, PONTO_FIM) < RAIO:
        return True
    if any(not verifica_intervalo(novo_centro, obstaculo[0]) for obstaculo in mapa_obstaculos):
        return True
    return False

def posicionar_obstaculos():
    for _ in range(QUANT_OBSTACULOS):
        tentativas = 0
        while True:
            tentativas += 1
            if tentativas >= 1000:
                print(f"Não há mais espaço! Foram posicionados {len(mapa_obstaculos)} obstáculos.")
                return  # Sai do posicionamento, mas mantém os já posicionados
            x = random.uniform(RAIO, TAMANHO_DO_PLANO - RAIO)
            y = random.uniform(RAIO, TAMANHO_DO_PLANO - RAIO)
            novo_centro = (x, y)
            if gerar_obstaculo_existente(novo_centro):
                continue
            mapa_obstaculos.append((novo_centro, calcular_laterais(novo_centro)))
            break

def reta_livre_de_obstaculos(A, B, mapa_obstaculos, raio):
    for obstaculo in mapa_obstaculos:
        centro = obstaculo[0]
        laterais = obstaculo[1]
        
        # 1. Se A e B são laterais do mesmo círculo, bloqueia
        if A in laterais and B in laterais:
            return False
            
        # 2. Coeficientes da reta AB: ax + by + c = 0
        r_a = B[1] - A[1]
        r_b = A[0] - B[0] 
        r_c = B[1] * (B[0] - A[0]) - (B[1] - A[1]) * B[0]

        # 3. Distância do centro do círculo à reta
        dist_reta = calcular_distancia_reta(r_a, r_b, r_c, centro[0], centro[1])
        
        # 4. Se a distância for menor que o raio, há interseção
        if dist_reta < raio:
            # 5. Verifica se a interseção está no segmento AB (não na reta infinita)
            # Calcula o ponto mais próximo do centro na reta AB
            denominador = r_a * r_a + r_b * r_b
            if denominador != 0:
                px = (r_b * (r_b * centro[0] - r_a * centro[1]) - r_a * r_c) / denominador
                py = (r_a * (-r_b * centro[0] + r_a * centro[1]) - r_b * r_c) / denominador
                
                # Verifica se o ponto projetado está dentro do segmento AB
                min_x, max_x = min(A[0], B[0]), max(A[0], B[0])
                min_y, max_y = min(A[1], B[1]), max(A[1], B[1])
                
                if min_x <= px <= max_x and min_y <= py <= max_y:
                    return False
    return True

def gerar_arestas():
    # Gera todas as arestas válidas e as adiciona aos obstáculos
    # Formato: [ponto_centro, [pontos_laterais], [arestas]]
    
    # Primeiro, inicializa a lista de arestas para cada obstáculo
    for i, obstaculo in enumerate(mapa_obstaculos):
        if len(obstaculo) == 2:  # Se ainda não tem arestas
            mapa_obstaculos[i] = (obstaculo[0], obstaculo[1], [])
    
    # Arestas do início aos pontos laterais
    for obstaculo in mapa_obstaculos:
        for ponto_lateral in obstaculo[1]:
            if reta_livre_de_obstaculos(PONTO_INICIO, ponto_lateral, mapa_obstaculos, RAIO):
                aresta = (PONTO_INICIO, ponto_lateral, 'blue', '--')
                arestas_globais.append(aresta)
    
    # Arestas do fim aos pontos laterais
    for obstaculo in mapa_obstaculos:
        for ponto_lateral in obstaculo[1]:
            if reta_livre_de_obstaculos(PONTO_FIM, ponto_lateral, mapa_obstaculos, RAIO):
                aresta = (PONTO_FIM, ponto_lateral, 'red', '--')
                arestas_globais.append(aresta)
    
    # Arestas entre pontos laterais (evita duplicação)
    for i, obstaculo_a in enumerate(mapa_obstaculos):
        for j, obstaculo_b in enumerate(mapa_obstaculos):
            if i >= j:  # Evita duplicação (só processa i < j)
                continue
            for ponto_lateral_a in obstaculo_a[1]:
                for ponto_lateral_b in obstaculo_b[1]:
                    if reta_livre_de_obstaculos(ponto_lateral_a, ponto_lateral_b, mapa_obstaculos, RAIO):
                        aresta = (ponto_lateral_a, ponto_lateral_b, 'green', '-')
                        # Adiciona à lista do primeiro obstáculo
                        mapa_obstaculos[i] = (mapa_obstaculos[i][0], mapa_obstaculos[i][1], mapa_obstaculos[i][2] + [aresta])
    
    # Verifica caminho direto início-fim
    if reta_livre_de_obstaculos(PONTO_INICIO, PONTO_FIM, mapa_obstaculos, RAIO):
        aresta = (PONTO_INICIO, PONTO_FIM, 'purple', '-')
        arestas_globais.append(aresta)


def inicializar_plot():
    fig, ax = plt.subplots()
    ax.set_xlim(0, TAMANHO_DO_PLANO)
    ax.set_ylim(0, TAMANHO_DO_PLANO)
    ax.set_aspect('equal')
    ax.grid(color='gray', linestyle='--', alpha=0.3)
    ax.axhline(0, color='white', linewidth=0.5)
    ax.axvline(0, color='white', linewidth=0.5)
    ax.plot(PONTO_INICIO[0], PONTO_INICIO[1], 'go', markersize=10, label='Início')
    ax.plot(PONTO_FIM[0], PONTO_FIM[1], 'ro', markersize=10, label='Fim')
    
    # Opção 2: Colocar fora da figura (à direita)
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1.0), frameon=True)
    plt.tight_layout()  # Ajusta automaticamente para não cortar
    
    return fig, ax

def plotar_obstaculos():
    # Inicializa o plot com início e fim
    _,ax = inicializar_plot()
    
    # Desenha todos os obstáculos
    for obstaculo in mapa_obstaculos:
        circulo = plt.Circle(obstaculo[0], RAIO, color="gray", alpha=0.7)
        for ponto in obstaculo[1]:
            ax.plot(ponto[0], ponto[1], 'o', markersize=2, color="black")
        ax.add_patch(circulo)
    
    plotar_arestas(ax)
    
    plt.title('Mapa de Obstáculos')
    plt.show()

def plotar_arestas(ax):
    # Plota arestas globais (início/fim)
    for aresta in arestas_globais:
        ponto_a, ponto_b, cor, estilo = aresta
        ax.plot([ponto_a[0], ponto_b[0]], [ponto_a[1], ponto_b[1]], 
                color=cor, linestyle=estilo, alpha=0.7)
    
    # Plota arestas dos obstáculos
    for obstaculo in mapa_obstaculos:
        if len(obstaculo) > 2:  # Se tem arestas
            for aresta in obstaculo[2]:
                ponto_a, ponto_b, cor, estilo = aresta
                ax.plot([ponto_a[0], ponto_b[0]], [ponto_a[1], ponto_b[1]], 
                        color=cor, linestyle=estilo, alpha=0.2)


def main():
    posicionar_obstaculos()
    gerar_arestas()
    print(f"Posicionados {len(mapa_obstaculos)} obstáculos")
    plotar_obstaculos()

if __name__ == "__main__":
    main()

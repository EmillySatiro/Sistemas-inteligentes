import matplotlib
matplotlib.use('Agg')  # Backend não-interativo para evitar problemas de GUI
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import numpy as np
import pickle
import shutil
import random
import os

# Configuração do matplotlib
plt.rcParams['figure.figsize'] = [4, 4]
plt.rcParams['figure.dpi'] = 100

# Parâmetros globais
tamanho = (100, 100)
ponto_inicial_final = (0, 0), tamanho
raio_size = 10
visual_s = 5
qtd_centroides = 10
paciencia = 10

def posicoes_circulos(x, y, raio_size):
    """Calcula as posições dos 4 pontos laterais de um círculo."""
    valor_baixo = (x, y - raio_size)
    valor_cima = (x, y + raio_size)
    valor_esquerda = (x - raio_size, y)
    valor_direita = (x + raio_size, y)
    return valor_baixo, valor_cima, valor_esquerda, valor_direita

def salvar_fig_ax(fig, ax, caminho='criacao_base/'):
    """Salva figura e eixos em arquivo pickle."""
    with open(f"{caminho}.pkl", "wb") as f:
        pickle.dump((fig, ax), f)

def abrir_fig_ax(caminho='criacao_base/'):
    """Carrega figura e eixos de arquivo pickle."""
    with open(f"{caminho}.pkl", "rb") as f:
        fig, ax = pickle.load(f)
    return fig, ax

def exibir_figura(figura, wait=False, pause=False, save=False, show=False):
    """Controla a exibição da figura."""
    if wait:
        plt.waitforbuttonpress()
    if pause:
        plt.pause(0.001)
    if show:
        figura.show()
    if save:
        figura.savefig("criacao_basefigura.png")

def inserir_circulo_img(ax, x, y, raio_size, visual_s, color_centro, color_ext):
    """Insere um círculo no gráfico com seus pontos laterais."""
    posicoes = posicoes_circulos(x, y, raio_size)
    valores_adicionados = []
    [valores_adicionados.append(ax.scatter(*posicao, color=color_ext, s=visual_s)) for posicao in posicoes]
    valores_adicionados.append(ax.scatter(x, y, color=color_centro, s=visual_s))
    valores_adicionados.append(plt.Circle((x, y), raio_size, color=color_ext, fill=False))
    ax.add_patch(valores_adicionados[-1])
    return valores_adicionados, posicoes

def distancia_euclidiana(ponto1, ponto2):
    """Calcula a distância euclidiana entre dois pontos."""
    x1, y1 = ponto1
    x2, y2 = ponto2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def verificar_distancia(x1, y1, x2, y2, raio_size) -> bool:
    """Verifica se dois pontos estão muito próximos considerando o raio."""
    return distancia_euclidiana((x1, y1), (x2, y2)) < 2 * raio_size

def coeficientes_reta(ponto_inicial, ponto_final):
    """
    Calcula os coeficientes da equação da reta que passa pelos pontos iniciais e finais.
    a -> coeficiente angular (inclinação)
    b -> coeficiente linear (intercepto)
    c -> termo constante

    link do exemplo: https://www.todamateria.com.br/equacao-da-reta/
    link da video aula: https://www.youtube.com/watch?v=9dhtGUPgekw

    é possivel transformar a equação da reta na forma y = mx + b, onde m é o coeficiente angular e b é o coeficiente linear.
    
    p1 = (-1, 8)
    p2 = (-5, -1)

    exemplo: 
    a = 9
    b = -4
    c = 41
    """
    a = (ponto_inicial[1] - ponto_final[1])
    b = (ponto_final[0] - ponto_inicial[0])
    c = (ponto_final[1] * ponto_inicial[0]) - (ponto_final[0] * ponto_inicial[1])
    return a, b, c

def distancia_ponto_reta(novo_ponto, a, b, c):
    """
    Calcula a distância do ponto (novo_ponto) à reta definida pelos coeficientes a, b e c.
    A fórmula é dada por: |ax + by + c| / sqrt(a^2 + b^2)

    Link exemplo: https://www.todamateria.com.br/distancia-entre-dois-pontos/
    Link video aula: https://www.youtube.com/watch?v=FSfwY1fM4EI
    
    Por que não usar a formula: 
    '
    distancia_x = x2 - x1
    distancia_y = y2 - y1
    distancia_euclidiana = (distancia_x ** 2 + distancia_y ** 2) ** 0.5
    '

    Motivo: 
    A fórmula da distância entre dois pontos é uma medida direta da distância euclidiana, 
    que é a mais comum em um espaço cartesiano. No entanto, quando se trata de calcular a distância de um ponto a uma linha,
    a fórmula da linha é mais apropriada, pois leva em consideração a inclinação da linha e a posição do ponto em relação a ela.
    
    Falando de forma informal: 
    Eles medem coisas diferentes. A distância ponto-reta nunca vai ser a mesma que a distância entre dois pontos específicos, porque:
    Uma compara ponto com ponto, A outra compara ponto com linha infinita.
    """
    divisor = ((a**2 + b**2) ** 0.5)
    if divisor == 0:
        raise ZeroDivisionError("Não é uma reta válida, mas sim o plano inteiro ou um conjunto vazio logo não é possível calcular a distância.")
    return abs(a * novo_ponto[0] + b * novo_ponto[1] + c) / divisor

def projecao_no_segmento(p: tuple[int, int], a: int, b: int, c: int, p1: tuple[int, int], p2: tuple[int, int]) -> tuple[float, float] | None:
    """
    Retorna a projeção ortogonal do ponto p sobre a reta definida por (a, b, c),
    mas somente se a projeção cair dentro do segmento [p1, p2].
    Caso contrário, retorna None.
    
    link aula: https://www.youtube.com/watch?v=fem35PVZjeA
    link solução:  https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
    

    oque é o denominador?
    O denominador é a soma dos quadrados dos coeficientes a e b da reta.
    Ele é usado para calcular as coordenadas da projeção ortogonal do ponto p na reta.
    Se o denominador for zero, significa que a reta é vertical (ou seja, a = 0 e b = 0), e a projeção não pode ser calculada.
    
    Falando de forma leiga:
    Estamos trabalhando com sombras, onde a reta é a superfície e o ponto p é a fonte de luz. A projeção ortogonal é a "sombra" do ponto p na reta.
    Isso significa que estamos tentando encontrar o ponto na reta que está diretamente abaixo do ponto p, como se estivéssemos projetando a luz do ponto p na reta.
    """
    x, y = p
    denominador = a*a + b*b
    if denominador == 0:
        raise ValueError("Coeficientes inválidos para reta.")

    px = (b * (b*x - a*y) - a*c) / denominador
    py = (a * (-b*x + a*y) - b*c) / denominador

    # Verifica se a projeção está dentro do segmento
    min_x, max_x = min(p1[0], p2[0]), max(p1[0], p2[0])
    min_y, max_y = min(p1[1], p2[1]), max(p1[1], p2[1])

    if abs(px - x) < 1e-9 and abs(py - y) < 1e-9:
        return None

    if min_x <= px <= max_x and min_y <= py <= max_y:
        return px, py
    return None

def reta_entre_dois_pontos(centroids: list[tuple], novo_ponto: tuple[int, int], novo_destino: tuple[int, int]):
    """
    Verifica se é possivel ter uma reta entre dois pontos sem que um centróide a intercepte.
    """
    a, b, c = coeficientes_reta(novo_ponto, novo_destino)
    for centroid in centroids:
        
        try:
            distancia = distancia_ponto_reta(centroid, a, b, c)
        except ZeroDivisionError:
            return False
        
        if distancia < raio_size:
            if (centroid[0] - novo_ponto[0]) * (novo_destino[1] - novo_ponto[1]) == (centroid[1] - novo_ponto[1]) * (novo_destino[0] - novo_ponto[0]):
                # print("Centróide está na reta")
                return False

            if projecao_no_segmento(centroid, a, b, c, novo_ponto, novo_destino):
                # print("Centróide está na projeção da reta")
                return False

    return True

def encontrar_possibilidades(pontos_unicos, ponto_inicial, ponto_final):
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
        for neighbor in pontos_unicos.get(current, []):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    
    return None

def ponto_mesmo_centroid(ponto1, ponto2, centroids, raio_size):
    """Verifica se dois pontos pertencem ao mesmo centróide."""
    centroid_ponto = None
    for i, centroid in enumerate(centroids):
        if distancia_euclidiana(ponto1, centroid) <= raio_size and distancia_euclidiana(ponto2, centroid) <= raio_size:
            centroid_ponto = i
            break

    return (True, centroids[centroid_ponto]) if centroid_ponto is not None else (False, None)

def main():
    """Função principal que executa todo o algoritmo."""
    # Preparar diretório
    shutil.rmtree('criacao_base', ignore_errors=True)
    os.makedirs('criacao_base', exist_ok=True)
    
    # Inicializar figura
    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    ax.scatter(*ponto_inicial_final[0], color='green', s=visual_s)
    ax.scatter(*ponto_inicial_final[1], color='red', s=visual_s)
    salvar_fig_ax(fig, ax)
    
    # Gerar centroids (obstáculos)
    centroids = []
    posicoes_centroides = []
    interacao_atual = 0
    paciencia_atual = 0
    
    while len(centroids) < qtd_centroides and paciencia_atual < paciencia:
        interacao_atual += 1
        paciencia_atual += 1
        
        x = random.randint(raio_size, tamanho[0] - raio_size)
        y = random.randint(raio_size, tamanho[1] - raio_size)

        if verificar_distancia(x, y, *ponto_inicial_final[0], raio_size):
            continue
        elif verificar_distancia(x, y, *ponto_inicial_final[1], raio_size):
            continue
        elif any(verificar_distancia(centroid[0], centroid[1], x, y, raio_size) for centroid in centroids):
            continue
        else:
            _, posicao_circulo = inserir_circulo_img(ax, x, y, raio_size, visual_s, 'blue', 'black')
            centroids.append((x, y))
            posicoes_centroides.append(posicao_circulo)
            paciencia_atual = 0
    
    salvar_fig_ax(fig, ax)
    
    print(f"Centroids criados: {len(centroids)}")
    print(f"Tentativas realizadas: {interacao_atual}")
    
    # Criar lista de todos os pontos
    todos_pontos = [ponto_inicial_final[0]]
    for x in range(len(posicoes_centroides)):
        for y in range(len(posicoes_centroides[x])):
            todos_pontos.append(posicoes_centroides[x][y])
    todos_pontos.append(ponto_inicial_final[1])
    
    # Gerar arestas válidas entre obstáculos diferentes
    retas = []
    for i in range(len(todos_pontos)):
        for j in range(i+1, len(todos_pontos)):
            if reta_entre_dois_pontos(centroids, todos_pontos[i], todos_pontos[j]):
                retas.append((todos_pontos[i], todos_pontos[j]))
    
    # Adicionar arestas internas dos obstáculos (diagonais)
    for (cima, baixo, esq, dir) in posicoes_centroides:
        retas.append((cima, esq))
        retas.append((cima, dir))
        retas.append((baixo, esq))
        retas.append((baixo, dir))
    
    # Desenhar todas as arestas
    fig, ax = abrir_fig_ax()
    for reta in retas:
        ax.plot(*zip(*reta), color='blue', alpha=0.6, linewidth=0.5)
    
    print(f"Total de pontos: {len(todos_pontos)}")
    print(f"Total de retas criadas: {len(retas)}")
    
    # Construir grafo de conectividade
    pontos_unicos = {}
    for reta in retas:
        pontos_unicos.setdefault(reta[0], set()).add(reta[1])
        pontos_unicos.setdefault(reta[1], set()).add(reta[0])  # Bidirecional
    
    # Buscar caminho
    ponto_inicial = ponto_inicial_final[0]
    ponto_final = ponto_inicial_final[1]
    
    pilha = encontrar_possibilidades(pontos_unicos, ponto_inicial, ponto_final)
    
    if pilha:
        print(f"Caminho encontrado com {len(pilha)} pontos!")
        print("Caminho:", pilha)
        
        # Desenhar o caminho encontrado
        for i in range(len(pilha) - 1):
            ponto1 = pilha[i]
            ponto2 = pilha[i + 1]

            mesmo_centro, centroid = ponto_mesmo_centroid(ponto1, ponto2, centroids, raio_size)
            if mesmo_centro:
                # Desenhar arco ao redor do obstáculo
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
                          theta1=theta1, theta2=theta2, color="green", linewidth=3)
                ax.add_patch(arco)
            else:
                # Desenhar linha reta entre obstáculos
                ax.plot([ponto1[0], ponto2[0]], [ponto1[1], ponto2[1]], 
                       color='red', linewidth=3)
        
        # Destacar pontos do caminho
        for ponto in pilha:
            ax.plot(ponto[0], ponto[1], 'yo', markersize=8, markeredgecolor='black', markeredgewidth=1)
        
        plt.title('Caminho Encontrado!')
        plt.savefig('caminho_encontrado.png', dpi=150, bbox_inches='tight')
        print("Figura salva como 'caminho_encontrado.png'")
        
    else:
        print("Nenhum caminho encontrado!")
        plt.title('Nenhum Caminho Encontrado!')
        plt.savefig('nenhum_caminho.png', dpi=150, bbox_inches='tight')
        print("Figura salva como 'nenhum_caminho.png'")

if __name__ == "__main__":
    main()
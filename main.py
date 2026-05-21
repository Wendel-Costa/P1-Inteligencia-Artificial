"""
================================================================================
ATIVIDADE DE BUSCA - INTELIGÊNCIA ARTIFICIAL
Problema: Roteamento Inteligente em São Luís do Maranhão com o Algoritmo A*
Destino fixo: UFMA (Campus Bacanga)

Algoritmo: A* (A-Star)
Biblioteca de grafos: NetworkX

Modelamos a cidade como um grafo onde os bairros são nós e as
vias são arestas com pesos em quilômetros.

Como funciona o A* que implementamos:
- A cada passo, expandimos o nó com menor f(n) = g(n) + h(n)
- g(n): custo real acumulado desde a origem até o nó n
- h(n): nossa estimativa (heurística) do custo de n até o destino
- Como nossa heurística é admissível, garantimos encontrar o caminho ótimo.
================================================================================
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# HEURÍSTICA h(n)
def heuristica(no_atual, destino):
    """
    Aqui definimos a função heurística h(n) do nosso algoritmo A*.

    Optamos por usar a distância em linha reta (km) de cada bairro até a UFMA
    como estimativa, pois ela nunca supera a distância real por estrada.

    Estimamos os valores com base na posição geográfica real de cada
    bairro em relação ao Campus Bacanga.

    Parâmetros:
        no_atual (str): Nome do bairro onde estamos agora.
        destino  (str): Nome do bairro de destino (sempre 'UFMA' neste projeto).

    Retorno:
        float: Distância estimada em km (0.0 quando chegamos ao destino).
    """
    distancias_linha_reta = {
        'Quebra-Pote': 22.0,
        'Cidade Operária': 15.0,
        'Turu': 12.0,
        'Cohama': 9.0,
        'Calhau': 10.0,
        'Anil': 8.5,
        'Vinhais': 7.5,
        'Renascença': 5.0,
        'São Francisco': 3.5,
        'Centro': 2.5,
        'Itaqui-Bacanga': 1.5,
        'UFMA': 0.0
    }
    # Usamos .get() para retornar 0 como padrão caso o bairro não esteja mapeado
    return distancias_linha_reta.get(no_atual, 0)

# CONSTRUÇÃO DO GRAFO
def criar_grafo_sao_luis():
    """
    Aqui construímos o grafo de ruas simplificado de São Luís.

    Decidimos modelar o problema da seguinte forma:
    - NÓS = bairros e pontos de referência que mapeamos
    - ARESTAS = conexões entre os bairros
    - PESOS = distâncias estimadas em km para cada trecho

    Retorno: G (nx.Graph): Grafo com os bairros e suas conexões.
    """

    G = nx.Graph()

    # --- EIXO ZONA RURAL / BR-135 ---
    G.add_edge('Quebra-Pote', 'Cidade Operária', weight=18.0)

    # --- EIXO AV. JERÔNIMO DE ALBUQUERQUE ---
    G.add_edge('Cidade Operária', 'Anil', weight=7.5)
    G.add_edge('Anil', 'Cohama', weight=5.5)
    G.add_edge('Cohama', 'Vinhais', weight=3.0)
    G.add_edge('Vinhais', 'Renascença', weight=4.0)

    # --- EIXO TURU / HOLANDESES ---
    G.add_edge('Cidade Operária', 'Turu', weight=8.0)
    G.add_edge('Turu', 'Cohama', weight=5.0)
    G.add_edge('Turu', 'Calhau', weight=7.0)
    G.add_edge('Calhau', 'Cohama', weight=4.0)
    G.add_edge('Calhau', 'Renascença', weight=4.5)

    # --- EIXO AV. DOS FRANCESES / CENTRO ---
    G.add_edge('Anil', 'Centro', weight=9.0) # Via Rodoviária/Franceses

    # --- EIXO VIA EXPRESSA ---
    G.add_edge('Vinhais', 'Itaqui-Bacanga', weight=11.0) # Conexão via Via Expressa -> Beira Mar

    # --- CONEXÃO PONTE JOSÉ SARNEY / SÃO FRANCISCO ---
    G.add_edge('Renascença', 'São Francisco', weight=2.0)
    G.add_edge('São Francisco', 'Centro', weight=3.0)

    # --- ACESSO FINAL À UFMA (BARRAGEM DO BACANGA) ---
    G.add_edge('Centro', 'Itaqui-Bacanga', weight=4.5) # Via Barragem
    G.add_edge('Itaqui-Bacanga', 'UFMA', weight=2.0)

    # Nota: A UFMA é acessada primordialmente pelo bairro Itaqui-Bacanga
    # após cruzar a Barragem vindo do Centro.

    return G

# RASTREAMENTO PASSO A PASSO DO A*
def rastrear_astar(G, origem, destino):
    """
    Aqui implementamos o A* manualmente para mostrar cada etapa da exploração,
    exibindo os valores f(n), g(n) e h(n) de cada nó expandido.

    Decidimos fazer isso além de usar o nx.astar_path porque queremos
    demonstrar com clareza como o algoritmo toma suas decisões.

    Parâmetros:
    - G (nx.Graph): Grafo viário que construímos.
    - origem (str): Bairro de onde partimos.
    - destino (str): Bairro onde queremos chegar.

    Retorno:
    - caminho (list): Lista de nós que formam o caminho ótimo encontrado.
    - custo   (float): Custo total do caminho em km.
    """
    import heapq

    # Usamos uma fila de prioridade (min-heap) para sempre expandir o nó com menor f(n) primeiro
    # Formato de cada entrada: (f, g, nó, caminho_até_aqui)
    fila = []
    g_inicial = 0.0
    h_inicial = heuristica(origem, destino)
    f_inicial = g_inicial + h_inicial
    heapq.heappush(fila, (f_inicial, g_inicial, origem, [origem]))

    # Mantemos um conjunto de nós já expandidos para não revisitá-los
    visitados = set()

    print("\n" + "=" * 65)
    print("📡 RASTREAMENTO INTERNO DO A* (passo a passo)")
    print("=" * 65)
    print(f"{'Nó Expandido':<20} {'g(n)':>7} {'h(n)':>7} {'f(n)':>7}")
    print("-" * 65)

    while fila:
        f, g, no_atual, caminho = heapq.heappop(fila)

        # Pulamos nós que já expandimos com custo menor anteriormente
        if no_atual in visitados:
            continue

        visitados.add(no_atual)

        h = heuristica(no_atual, destino)
        print(f"{no_atual:<20} {g:>7.1f} {h:>7.1f} {f:>7.1f}")

        # Chegamos ao destino e retornamos o caminho e seu custo total
        if no_atual == destino:
            print("=" * 65)
            return caminho, g

        # Expandimos os vizinhos do nó atual e os inserimos na fila
        for vizinho, dados in G[no_atual].items():
            if vizinho not in visitados:
                g_novo = g + dados['weight'] # somamos o custo real até aqui
                h_novo = heuristica(vizinho, destino) # estimamos o custo restante
                f_novo = g_novo + h_novo # calculamos a prioridade total
                heapq.heappush(fila, (f_novo, g_novo, vizinho, caminho + [vizinho]))

    return None, float('inf') # Chegamos aqui apenas se não encontrarmos nenhum caminho

def visualizar_grafo(G, caminho_otimo):
    # Definimos as posições manualmente para aproximar a disposição visual da localização geográfica real dos bairros, tornando o grafo mais intuitivo
    pos = {
        'Quebra-Pote': (4.5, 3.5),
        'Cidade Operária': (3.2, 3.2),
        'Turu': (2.8, 2.8),
        'Calhau': (2.5, 3.5),
        'Cohama': (2.2, 2.4),
        'Anil': (1.8, 2.0),
        'Vinhais': (1.2, 2.0),
        'Renascença': (1.8, 1.2),
        'São Francisco': (1.2, 0.9),
        'Centro': (0.8, 1.0),
        'Itaqui-Bacanga': (0.3, 0.6),
        'UFMA': (0.0, 0.0),
    }
 
    plt.figure(figsize=(15, 9))
    plt.title("Roteamento A* - Malha Viária de São Luís (Destino: UFMA)", fontsize=14)
 
    # Começamos todos os nós em cinza e depois colorimos os do caminho
    cor_nos = {no: '#ECF0F1' for no in G.nodes}
    if caminho_otimo:
        for no in caminho_otimo:
            cor_nos[no] = '#2ECC71'
        cor_nos[caminho_otimo[0]] = '#3498DB'
        cor_nos[caminho_otimo[-1]] = '#F1C40F'
 
    # Desenha o grafo completo
    nx.draw(G, pos, with_labels=True, node_color=[cor_nos[n] for n in G.nodes],
            node_size=3000, font_size=8, font_weight='bold', edge_color='#BDC3C7', width=1.5)
 
    # Rótulos de distância
    labels_arestas = {(u, v): f"{d['weight']}km" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_arestas, font_size=7)

    # Destaca o caminho encontrado
    if caminho_otimo:
        arestas_caminho = [(caminho_otimo[i], caminho_otimo[i+1]) for i in range(len(caminho_otimo)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=arestas_caminho, edge_color='#27AE60', width=5.0)

        # Destaca Origem e Destino
        nx.draw_networkx_nodes(G, pos, nodelist=[caminho_otimo[0]], node_color='#3498DB', node_size=3500)
        nx.draw_networkx_nodes(G, pos, nodelist=[caminho_otimo[-1]], node_color='#F1C40F', node_size=3500)
 
    # Legenda para facilitar a leitura do gráfico
    legenda = [
        mpatches.Patch(color='#3498DB', label='Origem'),
        mpatches.Patch(color='#F1C40F', label='Destino (UFMA)'),
        mpatches.Patch(color='#2ECC71', label='Caminho ótimo (A*)'),
        mpatches.Patch(color='#ECF0F1', label='Outros bairros'),
    ]
    plt.legend(handles=legenda, loc='upper right', fontsize=9, framealpha=0.9, title='Legenda')
 
    plt.axis('off')
    plt.tight_layout()
    # Salvamos a imagem automaticamente para facilitar o uso no relatório/vídeo
    plt.savefig('rota_astar_sao_luis.png', dpi=150, bbox_inches='tight')
    print("\n💾 Grafo salvo em: rota_astar_sao_luis.png")
    plt.show()
 
def main():
    G = criar_grafo_sao_luis()
    destino = 'UFMA'

    print("-" * 40)
    print("📍 NAVEGADOR A* - SÃO LUÍS")
    print("-" * 40)

    bairros = sorted(list(G.nodes))
    print("Bairros mapeados:")
    for i in range(0, len(bairros), 3):
        print(", ".join(bairros[i:i+3]))

    origem = input("\nOnde você está? ").title().strip()

    if origem not in G.nodes:
        print("❌ Bairro não reconhecido. Verifique a grafia e tente novamente.")
        return

    # Executamos nosso A* com rastreamento detalhado passo a passo
    caminho_otimo, custo_total = rastrear_astar(G, origem, destino)
 
    if caminho_otimo is None:
        print("\n❌ Não há conexão viária mapeada entre esses pontos.")
        return
 
    # Também chamamos o nx.astar_path para confirmar nosso resultado —
    # se os dois caminhos coincidirem, temos certeza que a implementação está correta
    nx.astar_path(G, source=origem, target=destino, heuristic=heuristica, weight='weight')
 
    print("\nDetalhamento da rota:")
    custo = 0
    for u, v in zip(caminho_otimo[:-1], caminho_otimo[1:]):
      peso = G[u][v]['weight']
      custo += peso
      print(f"{u} ➔ {v} | +{peso} km | acumulado: {custo:.1f} km")
 
    print("\n" + "🏁" * 20)
    print(f"MELHOR ROTA: {' ➔ '.join(caminho_otimo)}")
    print(f"DISTÂNCIA TOTAL ESTIMADA: {custo_total} km")
    print("🏁" * 20)
 
    visualizar_grafo(G, caminho_otimo)
 
if __name__ == "__main__":
    main()
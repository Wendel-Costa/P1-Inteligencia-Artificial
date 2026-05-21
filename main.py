import networkx as nx
import matplotlib.pyplot as plt

def heuristica(no_atual, destino):
    """
    Estimativa de distância em linha reta (km) até a UFMA.
    Valores baseados na posição geográfica real em relação ao Campus Bacanga.
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
    return distancias_linha_reta.get(no_atual, 0)

def criar_grafo_sao_luis():
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

def visualizar_grafo(G, caminho_otimo):
    # Layout que tenta manter a relação espacial
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(15, 9))
    plt.title("Roteamento A* - Malha Viária de São Luís (Destino: UFMA)", fontsize=14)

    # Desenha o grafo completo
    nx.draw(G, pos, with_labels=True, node_color='#ECF0F1', node_size=3000,
            font_size=8, font_weight='bold', edge_color='#BDC3C7', width=1.5)

    # Rótulos de distância
    labels_arestas = {(u, v): f"{d['weight']}km" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_arestas, font_size=7)

    # Destaca o caminho encontrado
    if caminho_otimo:
        arestas_caminho = [(caminho_otimo[i], caminho_otimo[i+1]) for i in range(len(caminho_otimo)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=arestas_caminho, edge_color='#27AE60', width=5.0)
        nx.draw_networkx_nodes(G, pos, nodelist=caminho_otimo, node_color='#2ECC71', node_size=3200)

        # Destaca Origem e Destino
        nx.draw_networkx_nodes(G, pos, nodelist=[caminho_otimo[0]], node_color='#3498DB', node_size=3500)
        nx.draw_networkx_nodes(G, pos, nodelist=[caminho_otimo[-1]], node_color='#F1C40F', node_size=3500)

    plt.axis('off')
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

    try:
        caminho_otimo = nx.astar_path(G, source=origem, target=destino, heuristic=heuristica, weight='weight')
        custo_total = sum(G[u][v]['weight'] for u, v in zip(caminho_otimo[:-1], caminho_otimo[1:]))

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

    except nx.NetworkXNoPath:
        print("\n❌ Não há conexão viária mapeada entre esses pontos.")

if __name__ == "__main__":
    main()

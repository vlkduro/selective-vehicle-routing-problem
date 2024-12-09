import networkx as nx
import matplotlib

matplotlib.use('TkAgg')  # Nécessaire si une erreur de canva Tkinter à la compilation
import matplotlib.pyplot as plt
import random


def draw_graph(graph):
    pos = nx.spring_layout(G, k=20)  # Utilisation d'un seed pour une disposition stable

    # Dessiner le graphe
    plt.figure(figsize=(8, 8))  # Taille de la figure
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        node_size=800,
        font_size=10,
        font_color="black",
        font_weight="bold"
    )
    edge_labels = nx.get_edge_attributes(G, 'coût')  # Obtenir les poids
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(f"Graphe Complet à {graph.number_of_nodes()} nœuds", fontsize=15)
    plt.show()


def create_graph(n):
    # nombre de clients (noeuds)
    start = 'A'
    end = 'D'
    G = nx.complete_graph(n)
    G = nx.relabel_nodes(G, {0: start})
    G = nx.relabel_nodes(G, {len(G.nodes) - 1: end})
    for u, v in G.edges():
        G[u][v]['coût'] = random.randint(1, 30)
    return G


def gluttony(flotte, G):
    profit = []
    return profit


flotte = [1, 2]
G = create_graph(10)
draw_graph(G)

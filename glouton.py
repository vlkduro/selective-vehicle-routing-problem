import networkx as nx
import matplotlib

matplotlib.use('TkAgg')  # Nécessaire si une erreur de canva Tkinter à la compilation
import matplotlib.pyplot as plt
import random


def draw_graph(G, blocked):
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
    plt.title(f"Graphe Complet à {G.number_of_nodes()} nœuds", fontsize=15)
    plt.show(block=blocked)


def create_graph(n):
    # nombre de clients (noeuds)
    start = 'A'
    end = 'D'
    profit_dict = {}
    G = nx.complete_graph(n)
    G = nx.relabel_nodes(G, {0: start})
    G = nx.relabel_nodes(G, {len(G.nodes) - 1: end})
    for node in G.nodes:
        profit_dict[node] = random.randint(1, 100)
    for u, v in G.edges():
        G[u][v]['coût'] = random.randint(1, 30)
    return G, profit_dict


def gluttony(flotte, G, profit_dict, L):
    profit = {}  # Stocker les profits pour chaque véhicule
    trajets = {i: [] for i in flotte}  # Stocker les trajets pour chaque véhicule
    NonVisitedClient = list(G.nodes).copy()  # Liste des clients non visités
    print(NonVisitedClient)
    getAllProfit = 0
    for i in flotte:
        print(f"Flotte {i}")
        profit[i] = 0
        trajet = ['A']  # Commence toujours par 'A'
        totalCost = 0
        totalProfit = 0

        while NonVisitedClient:  # Tant qu'il reste des clients à visiter
            bestC = None
            bestP = 0

            for c in list(G.neighbors(trajet[-1])):  # Parcourt les voisins du dernier nœud
                if c in NonVisitedClient and c != 'D' and c != 'A':  # Ne pas revisiter les clients ou aller directement à 'D'
                    p = profit_dict[c]
                    distance_to_D = nx.shortest_path_length(G, source=c, target='D', weight='coût')
                    cost = G[trajet[-1]][c]['coût'] + distance_to_D

                    if totalCost + cost <= L and p > bestP:  # Vérifie les contraintes
                        bestC = c
                        bestP = p

            if bestC is not None:  # Si un client valide est trouvé
                trajet.append(bestC)
                totalCost += G[trajet[-2]][bestC]['coût']
                totalProfit += profit_dict[bestC]
                NonVisitedClient.remove(bestC)
                print(f"Visite de {bestC} par la flotte {i}, profit = {profit_dict[bestC]}")
            else:
                # Aucun client viable, termine le trajet pour ce véhicule
                break

        # Ajoute 'D' (destination finale) si possible
        if totalCost + nx.shortest_path_length(G, source=trajet[-1], target='D', weight='coût') <= L:
            trajet.append('D')

        trajets[i] = trajet  # Enregistre le trajet pour ce véhicule
        profit[i] = totalProfit  # Enregistre le profit total pour ce véhicule
        getAllProfit += totalProfit
        print(f"Trajet pour flotte {i} : {trajet}, profit total = {totalProfit}, pour un coût = {totalCost}")

    return profit, trajets, getAllProfit

flotte1 = [1, 2]  # Une flotte de 2 véhicules
L = 30 # Chaque véhicule possède une longueur max de 30
G, profit_dict = create_graph(10)
print("Algorithme glouton pour la flotte 1")
_, _, getAll = gluttony(flotte1, G, profit_dict, L)
print("===========")
print("Le profit obtenu pour une flotte avec", len(flotte1), "véhicules: ", getAll)
print("=FIN=")
draw_graph(G, "false")


flotte2 = [1, 2, 3, 4, 5]  # Une flotte de 5 véhicules
M = 10 # Chaque véhicule possède une longueur max de 10
H, profit_dict2 = create_graph(20)
print("Algorithme glouton pour la flotte 2")
_, _, getAll = gluttony(flotte2, H, profit_dict2, M)
print("===========")
print("Le profit obtenu pour une flotte avec", len(flotte2), "véhicules: ", getAll)
print("=FIN=")
draw_graph(H, "false")

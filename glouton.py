import networkx as nx
import matplotlib

matplotlib.use('TkAgg')  # Nécessaire si une erreur de canva Tkinter à la compilation
import matplotlib.pyplot as plt
import random
import time


def draw_graph(G, blocked):
    if G.number_of_nodes() < 30 :
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
    else :
        pos = nx.spring_layout(G, k=40)  # Utilisation d'un seed pour une disposition stable

        # Dessiner le graphe
        plt.figure(figsize=(24, 24))  # Taille de la figure
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
        j = 0 # Index pour répérer le temps max de trajet pour i.
        print(f"Flotte {i}")
        profit[i] = 0
        trajet = ['A']  # Commence toujours par 'A'
        totalCost = 0
        totalProfit = 0

        while NonVisitedClient:  # Tant qu'il reste des clients à visiter
            bestC = None
            bestP = 0

            for c in list(G.neighbors(trajet[-1])):  # Parcourt les voisins du dernier nœud
                if c in NonVisitedClient and c != 'D' and c != 'A':  # Un client n'est visitable qu'une fois, d
                    # de même on ne repasse pas par A
                    p = profit_dict[c]
                    distance_to_D = nx.shortest_path_length(G, source=c, target='D', weight='coût') # Fonction networkX
                    cost = G[trajet[-1]][c]['coût'] + distance_to_D # Le coût est la distance vers le voisin
                    # Si le coût empêche d'arriver jusqu'a D on élimine cette possibilité
                    if totalCost + cost <= L[j] and p > bestP:  # Vérifie les contraintes
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
        if totalCost + nx.shortest_path_length(G, source=trajet[-1], target='D', weight='coût') <= L[j]:
            trajet.append('D')

        trajets[i] = trajet  # Enregistre le trajet pour ce véhicule
        profit[i] = totalProfit  # Enregistre le profit total pour ce véhicule
        getAllProfit += totalProfit
        print(f"Trajet pour véhicule {i} : {trajet}, profit total = {totalProfit}, pour un coût = {totalCost}")
        j += 1

    return profit, trajets, getAllProfit


start = time.time()
print("=========Algorithme glouton pour la flotte 1========")
flotte1 = [1, 2]  # Une flotte de 2 véhicules
L = []
for i in range(len(flotte1)):
    L.append(random.randint(10,30))
    print(f"Le coût max du véhicule {i+1} est {L[i]}") # Chaque véhicule possède une longueur max randomisée
G, profit_dict = create_graph(10)
_, _, getAll = gluttony(flotte1, G, profit_dict, L)
print("===========")
print("Le profit obtenu pour une flotte avec", len(flotte1), "véhicules: ", getAll)
print("====FIN====")
execution_time1 = time.time() - start
print(f"Exécution time for {G.number_of_nodes()} nodes and {len(flotte1)} vehicules = {execution_time1} ms")
draw_graph(G, "false")

start = time.time()
print("=========Algorithme glouton pour la flotte 2========")
flotte2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Une flotte de 10 véhicules
M = []
for i in range(len(flotte1)):
    M.append(random.randint(5,30))
    print(f"Le coût max du véhicule {i+1} est {M[i]}") # Chaque véhicule possède une longueur max randomisée
H, profit_dict = create_graph(100)
_, _, getAll = gluttony(flotte2, H, profit_dict, M)
print("===========")
print("Le profit obtenu pour une flotte avec", len(flotte2), "véhicules: ", getAll)
print("====FIN====")
execution_time2 = time.time() - start
print(f"Exécution time for {H.number_of_nodes()} nodes and {len(flotte2)} vehicules = {execution_time2} ms")
draw_graph(H, "false")



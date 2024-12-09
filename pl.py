import matplotlib
matplotlib.use('TkAgg')  # Utilise TkAgg comme backend

import matplotlib.pyplot as plt
import numpy as np
import xpress as xp
import itertools

# Nombre de clients
n_clients = 15

# Positions des clients et points de départ (a) et d'arrivée (d)
points = {
    'a': (0, 0, 0),  # Point de départ
    'd': (10, 10, 0),  # Point d'arrivée
}

# Génération de positions aléatoires pour les clients ainsi que le gain associé (3ème chiffre)
np.random.seed(50)  # Pour la reproductibilité
for i in range(1, n_clients + 1):
    points[i] = (np.random.randint(1, 10), np.random.randint(1, 10), np.random.randint(1, 100))

# Calculer les distances entre les points (euclidienne)
def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Calculer la matrice des distances
C = {}
for i in points:
    for j in points:
        if i != j:
            C[(i, j)] = distance(points[i], points[j])

# Affichage sous forme de tableau
print(C)

# Définir les gains associés aux clients
P = {i: points[i][2] for i in range(1, n_clients + 1)}
print(P)
# Paramètres du problème
L = 15  # Distance limite par véhicule
m = 2  # Nombre de véhicules
n = len(points)  # Nombre de sommets (clients + points de départ et d'arrivée)

# Modélisation en programmation linéaire
model = xp.problem()

# Variables de décision
x = {(k, i, j): xp.var(vartype=xp.binary) for k in range(m) for i in points for j in points if i != j}
u = {(k, i): xp.var(vartype=xp.binary) for k in range(m) for i in points}

# Ajout des variables au modèle
model.addVariable(x)
model.addVariable(u)

# Objectif : Maximiser les profits
model.setObjective(
    xp.Sum(P[i] * u[k, i] for k in range(m) for i in points if i != 'a' and i != 'd'),
    sense=xp.maximize
)

# Contraintes

# Limite de distance (temps) par véhicule
for k in range(m):
    model.addConstraint(
        xp.Sum(C[i, j] * x[k, i, j] for i in points for j in points if i != j) <= L  # Pas plus de L par véhicule
    )

# Lier les variables u[k, i] et x[k, i, j] et ainsi obligé qu'il y ai 2 sur chaque sommet
for k in range(m):
    for i in points:
        if i not in ['a', 'd']:
            model.addConstraint(
                (2*u[k, i] == (xp.Sum(x[k, j, i] for j in points if j != i) + xp.Sum(x[k,i,j] for j in points if j != i)))
            )
    
#Démare par a
for k in range(m):
    model.addConstraint(
        xp.Sum(x[k, 'a', j] for j in points if j!='a') == 1
    )
    model.addConstraint(
        xp.Sum(u[k, 'a'] ) == 1
    )


#Fini par d
for k in range(m):
    model.addConstraint(
        xp.Sum(x[k, j, 'd'] for j in points if j!='d') == 1
    )
    model.addConstraint(
        xp.Sum(u[k, 'd'] ) == 1
    )

# Chaque sommet est visité une seul fois
for i in points:
    if i not in ['a', 'd']:
        model.addConstraint(
            xp.Sum(u[k, i] for k in range(m)) <= 1
        )

# Ajout des contraintes d'élimination des sous-tours
for k in range(m):
    for i, j in itertools.combinations([i for i in points], 2):
        # Contrainte pour empêcher le sous-tour : si on va de i à j, alors on ne peut pas revenir de j à i dans le même trajet
        model.addConstraint(
            x[k, i, j] + x[k, j, i] <= 1  # Si x[k, i, j] = 1, alors x[k, j, i] doit être 0
        )


# Résolution
model.solve()

# Résultats
# Vérification de la solution
routes = {k: [] for k in range(m)}  # Stocker les routes pour chaque véhicule
total_costs = {k: 0 for k in range(m)}  # Stocker les coûts totaux pour chaque véhicule
total_profits = {k: 0 for k in range(m)}  # Stocker les gains totaux pour chaque véhicule

print("\nSolution optimale trouvée :")
for k in range(m):
    print(f"\nVéhicule {k+1}:")
    for i in points:
        for j in points:
            if i != j and model.getSolution(x[k, i, j]) > 0.5:
                routes[k].append((i, j))
                cost = C[i, j]  # Coût pour le chemin de i à j
                total_costs[k] += cost
                print(f" - Traverse de {i} à {j} (Coût : {cost})")
    
    # Calcul des gains des clients pour ce véhicule
    vehicle_profit = sum(
        P[i] * model.getSolution(u[k, i]) for i in points if i != 'a' and i != 'd'
    )
    total_profits[k] = vehicle_profit

    # Affichage des totaux
    print(f"  Coût total pour le véhicule {k+1} : {total_costs[k]}")
    print(f"  Gain total pour le véhicule {k+1} : {total_profits[k]}")

# Calcul des totaux globaux
total_cost = sum(total_costs.values())
total_profit = sum(total_profits.values())

# Résumé global
print("\nRésumé global :")
print(f"Coût total : {total_cost}")
print(f"Gain total : {total_profit}")

# Visualisation du graphe
plt.figure(figsize=(8, 8))
colors = ['blue', 'green', 'red', 'orange', 'purple']  # Couleurs pour les véhicules

# Tracer les points
for i in points:
    plt.scatter(points[i][0], points[i][1], label=f"{i} ({points[i][2]})", s=100)

# Tracer les lignes pour chaque véhicule
for k, route in routes.items():
    for (i, j) in route:
        plt.plot([points[i][0], points[j][0]], [points[i][1], points[j][1]], color=colors[k % len(colors)], linestyle='-', linewidth=2)

# Ajouter des labels pour chaque point (exclure 'a' et 'd')
for i in points:
    if i not in ['a', 'd']:
        plt.text(points[i][0] + 0.3, points[i][1], f"{P[i]}", fontsize=12)
    else :
        plt.text(points[i][0] + 0.3, points[i][1], f"{i}", fontsize=12)


# Légende
plt.legend()
plt.title("Solution du problème de VRP")
plt.show()

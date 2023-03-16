from pulp import *

# Définir les données d'entrée
equipements = ['E1', 'E2', 'E3', 'E4']  # Liste des équipements à entretenir
corps_metiers = ['CM1', 'CM2', 'CM3']  # Liste des corps de métier
intervalles = {'CM1': 14, 'CM2': 21, 'CM3': 30}  # Intervalles de maintenance par corps de métier (en jours)
temps_travail = {'CM1': 6, 'CM2': 8, 'CM3': 10}  # Temps de travail estimé par corps de métier (en heures)

# Définir le problème d'optimisation linéaire
prob = LpProblem("Maintenance_Preventive", LpMinimize)

# Définir les variables de décision
x = LpVariable.dicts("Maintenance", [(e, c) for e in equipements for c in corps_metiers], 0, 1, LpBinary)

# Définir la fonction objectif
prob += lpSum([x[(e, c)] * temps_travail[c] for e in equipements for c in corps_metiers])

# Contrainte : chaque équipement doit être maintenu au moins une fois pendant la période de planification
for e in equipements:
    prob += lpSum([x[(e, c)] for c in corps_metiers]) == 1

# Contrainte : la maintenance doit être effectuée dans l'intervalle spécifié pour chaque corps de métier
for c in corps_metiers:
    for i in range(0, len(equipements), intervalles[c]):
        prob += lpSum([x[(equipements[e], c)] for e in range(i, min(i+intervalles[c], len(equipements)))]) >= 1

# Résoudre le problème d'optimisation linéaire
prob.solve()

# Afficher les résultats
print("Statut de la résolution : {}".format(LpStatus[prob.status]))
print("Coût total : {} heures".format(round(value(prob.objective), 2)))

# Afficher la planification de maintenance par équipement et par corps de métier
for e in equipements:
    print("Equipement {} :".format(e))
    for c in corps_metiers:
        if x[(e, c)].value() == 1:
            print("- {} : {} heures".format(c, temps_travail[c]))

# Afficher la charge de travail par corps de métier
for c in corps_metiers:
    temps_total = sum([x[(e, c)].value() * temps_travail[c] for e in equipements])
    print("Charge de travail pour le corps de métier {} : {} heures".format(c, temps_total))
	


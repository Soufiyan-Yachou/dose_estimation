"""
Auteur : YACHOU Soufiyan
Email : soufiyanyachou@gmail.com
Description : Ce script effectue une estimation de dose en utilisant une courbe exponentielle décroissante.
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.optimize import curve_fit

# Données initiales pour la dose
pixels = np.array([])
doses = np.array([])

# Fonction exponentielle décroissante qui tend vers 0
def exp_decay(x, a, b):
    return a * np.exp(-b * x)

# Ajustement de la courbe exponentielle avec une décroissance plus rapide
popt, _ = curve_fit(exp_decay, pixels, doses)

# Estimation des valeurs jusqu'à 60 pixels
pixel_values = np.arange(0, 61)
estimated_doses = exp_decay(pixel_values, *popt)

# Forcer une décroissance rapide vers 0 pour les derniers pixels
# Ajustement manuel pour garantir que les dernières valeurs soient proches de 0
for i in range(len(estimated_doses)):
    if estimated_doses[i] < 1e-10:  # Seuil très bas pour ajuster les dernières valeurs à 0
        estimated_doses[i] = 0

# Calcul du pourcentage (par rapport à Vmax qui est la dose au pixel 0)
vmax = estimated_doses[0]
percentages = (estimated_doses / vmax) * 100

# Enregistrement des résultats dans un fichier CSV
with open('dose_estimation_output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Pixel', 'Dose (D(x))', 'Pourcentage (%)'])  # En-tête du tableau
    
    for i in range(len(pixel_values)):
        writer.writerow([pixel_values[i], f"{estimated_doses[i]:.10e}", f"{percentages[i]:.2f}"])

# Enregistrement des résultats dans un fichier texte (txt) avec les doses et pourcentages sous forme de liste
with open('dose_percent_output.txt', mode='w') as file:
    file.write("Doses = [\n")
    file.write(",\n".join([f"{dose:.10e}" for dose in estimated_doses]))
    file.write("\n]\n\n")
    
    file.write("Percentages = [\n")
    file.write(",\n".join([f"{percent:.2f}" for percent in percentages]))
    file.write("\n]\n")

# Affichage des résultats dans la console
for i in range(len(pixel_values)):
    print(f"Pixel {i}: Dose estimée = {estimated_doses[i]:.10e}, Pourcentage = {percentages[i]:.2f}%")

# Optionnel : Visualisation du résultat
plt.plot(pixel_values, estimated_doses, label='Estimation exponentielle décroissante rapide')
plt.scatter(pixels, doses, color='red', label='Données originales')
plt.xlabel('Pixel')
plt.ylabel('Dose')
plt.legend()
plt.show()


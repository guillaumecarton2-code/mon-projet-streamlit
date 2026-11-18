from pathlib import Path
import pandas as pd

# 1. Chargement du fichier
file_path = Path("data/cleaned/livres_auteurs_clean.csv")   # Chargement du fichier CSV nettoyé contenant les données brutes
df = pd.read_csv(file_path, low_memory=False)      # Chargement des données nettoyées

# 2. Classement global des auteurs les plus présents
# On compte le nombre d'œuvres (work_id) par auteur (author_id)
top_auteurs_global = (                     # création variable top_auteurs_global
    df.groupby("author_id")["work_id"]     # on regroupe par author_id et on sélectionne la colonne work_id
    .count()                               # on compte le nombre d'œuvres par auteur avec count()
    .reset_index(name="nombre_de_livres")  # on réinitialise l'index et on renomme la colonne résultante en "nombre_de_livres"
    .sort_values(by="nombre_de_livres", ascending=False)         # on trie les résultats par nombre de livres décroissant avec sort_values() et ascending=False
)

print("--- Top 10 des auteurs les plus présents (toutes contributions confondues) ---")
print(top_auteurs_global.head(10))
print(len(top_auteurs_global), "auteurs au total.")     # Affichage du nombre total d'auteurs présents dans le DataFrame après le regroupement et le comptage


# 3. Optionnel : Classement en ne gardant que l'auteur principal (ordre == 1)
# Utile pour éviter de sur-compter les co-auteurs ou les ouvrages collectifs
top_auteurs_principaux = (                         # création variable top_auteurs_principaux
    df[df["ordre"] == 1]                           # on filtre le DataFrame pour ne garder que les lignes où l'ordre est égal à 1, ce qui correspond à l'auteur principal
    .groupby("author_id")["work_id"]               # on regroupe par author_id et on sélectionne la colonne work_id
    .count()                                       # on compte le nombre d'œuvres par auteur principal avec count()
    .reset_index(name="nombre_de_livres_principaux")       # on réinitialise l'index et on renomme la colonne résultante en "nombre_de_livres_principaux"
    .sort_values(by="nombre_de_livres_principaux", ascending=False)   # on trie les résultats par nombre de livres principaux décroissant avec sort_values() et ascending=False
)

print("\n--- Top 10 des auteurs principaux (ordre == 1) ---")
print(top_auteurs_principaux.head(10))
print(len(top_auteurs_principaux), "auteurs principaux au total.")   # Affichage du nombre total d'auteurs principaux présents dans le DataFrame après le regroupement et le comptage
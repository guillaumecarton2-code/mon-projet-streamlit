from datetime import datetime
from pathlib import Path
import pandas as pd

# 1. Chargement des données brutes
input_path = Path("data/livres_auteurs.csv")  # Chargement du fichier CSV contenant les données brutes
df_brut = pd.read_csv(input_path, low_memory=False)  # Chargement des données brutes
nb_lignes_initial = len(df_brut)               # controle du nombre de lignes initiales avant nettoyage

# 2. Inspection des doublons (work_id, author_id) avant suppression
doublons_mask = df_brut.duplicated(subset=["work_id", "author_id"], keep=False) # création du masque de doublons
df_doublons = df_brut[doublons_mask].sort_values(
    by=["work_id", "author_id", "ordre"]
)                                           # création variable à partir des données brutes en appliquant le masque de doublons et tri par work_id, author_id, ordre

print(f"Nombre de lignes concernées par un doublon : {len(df_doublons)}")
if not df_doublons.empty:                                  # renvoie un booléen si df_doublons est vide avec condition if not qui inverse le booléen
  print("\nAperçu des doublons détectés (avant nettoyage) :")
  print(df_doublons.head(6))

# 3. Nettoyage : tri par 'ordre' croissant puis dédoublonnage sur (work_id, author_id)
df_clean = (                                  # création variable df_clean
    df_brut.sort_values(by="ordre", ascending=True)   # tri par ordre croissant
    .drop_duplicates(subset=["work_id", "author_id"], keep="first")  # suppression des doublons en gardant la première occurrence avec keep="first"
    .sort_index()  # Restaure l'ordre d'origine du fichier 
    .reset_index(drop=True)  # Réinitialise l'index pour avoir un index propre après le nettoyage
)

nb_lignes_final = len(df_clean)   # controle du nombre de lignes finales après nettoyage
nb_supprimes = nb_lignes_initial - nb_lignes_final  # calcul du nombre de doublons supprimés

# 4. Export du fichier nettoyé
output_dir = Path("data/cleaned")   # création du répertoire de sortie pour le fichier nettoyé
output_dir.mkdir(parents=True, exist_ok=True)   # création du répertoire de sortie s'il n'existe pas déjà
output_path = output_dir / "livres_auteurs_clean.csv"  # création du chemin complet pour le fichier nettoyé
df_clean.to_csv(output_path, index=False)  # sauvegarde du fichier nettoyé au format CSV sans l'index

print(f"\nNettoyage terminé : {nb_supprimes} doublons supprimés.")
print(
    f"Fichier sauvegardé : {output_path} ({nb_lignes_final} lignes conservées)."
)
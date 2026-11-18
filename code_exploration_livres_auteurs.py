from pathlib import Path
import pandas as pd

# chargement du fichier CSV
file_path = Path("Data/livres_auteurs.csv")  # chargement du fichier CSV contenant les données brutes
df = pd.read_csv(file_path, low_memory=False)  # chargement des données brutes

print("--- 1. Dimensions et structure ---")
print(f"Nombre de lignes : {df.shape[0]} | Nombre de colonnes : {df.shape[1]}")  # Affichage des dimensions avec axes shape[0] pour le nombre de lignes et shape[1] pour le nombre de colonnes
print(df.info())  # Affichage des informations sur le DataFrame, y compris les types de données et les valeurs manquantes

print("\n--- 2. Aperçu des premières lignes ---")
print(df.head(3))

print("\n--- 3. Valeurs manquantes (%)---")
missing = df.isna().sum()  # Calcul du nombre de valeurs manquantes par colonne avec isna().sum()
missing_pct = (missing / len(df)) * 100  # Calcul du pourcentage de valeurs manquantes par colonne en divisant le nombre de valeurs manquantes par le nombre total de lignes et en multipliant par 100
print(pd.DataFrame({"Valeurs manquantes": missing, "Pourcentage": missing_pct}))

print("\n--- 4. Statistiques de cardinalité ---")
for col in df.columns:                   # Boucle sur chaque colonne du DataFrame pour calculer le nombre de valeurs uniques
    unique_count = df[col].nunique()         # Calcul du nombre de valeurs uniques dans la colonne avec nunique()
    print(f"Colonne '{col}' : {unique_count} valeurs uniques")

# --- 5. Vérification des doublons ---
print("\n--- 5. Vérification des doublons ---")
duplicates = df.duplicated().sum()             # Calcul du nombre de doublons dans le DataFrame avec duplicated().sum()
print(f"Nombre de doublons complets : {duplicates}")
print("Doublons sur le couple (work_id, author_id) :"
      f" {df.duplicated(subset=['work_id', 'author_id']).sum()}")  # Calcul du nombre de doublons sur le couple (work_id, author_id) avec duplicated(subset=['work_id', 'author_id']).sum()
print("Doublons sur (work_id, ordre) :"
      f" {df.duplicated(subset=['work_id', 'ordre']).sum()}")    # Calcul du nombre de doublons sur le couple (work_id, ordre) avec duplicated(subset=['work_id', 'ordre']).sum()

# --- 6. Analyse de la distribution de 'ordre' et ouvrages collectifs ---
print("\n--- 6. Analyse de la distribution de 'ordre' et ouvrages collectifs ---")
print(f"Min : {df['ordre'].min()} | Max : {df['ordre'].max()}")       # Affichage des valeurs minimale et maximale de la colonne 'ordre' avec min() et max()
print(f"Nombre d'oeuvres avec ordre == 1 : {(df['ordre'] == 1).sum()}")   # Calcul du nombre d'oeuvres avec ordre == 1 en comparant la colonne 'ordre' à 1 et en sommant les valeurs True avec sum()

# Top 5 des oeuvres ayant le plus grand nombre d'auteurs
top_collectifs = df["work_id"].value_counts().head(5)     # Affichage des 5 oeuvres ayant le plus grand nombre d'auteurs en utilisant value_counts() sur la colonne 'work_id' et en sélectionnant les 5 premières valeurs avec head(5)
print("\nTop 5 des oeuvres avec le plus d'auteurs associés :")
print(top_collectifs)

# --- 7. Vérification du format des identifiants ---
print("\n--- 7. Validation du format Open Library ---")
valid_work = df["work_id"].str.match(r"^OL\d+W$").all()      # Vérification que tous les work_id respectent le format 'OL<chiffres>W' en utilisant str.match() avec une expression régulière et all() pour vérifier que toutes les valeurs sont True
valid_author = df["author_id"].str.match(r"^OL\d+A$").all()   # Vérification que tous les author_id respectent le format 'OL<chiffres>A' en utilisant str.match() avec une expression régulière et all() pour vérifier que toutes les valeurs sont True
print(f"Tous les work_id respectent le format 'OL<chiffres>W' : {valid_work}")
print(f"Tous les author_id respectent le format 'OL<chiffres>A' : {valid_author}")

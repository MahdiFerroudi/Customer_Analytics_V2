import pandas as pd

def create_categories_dict(csv_file):
    # Lire le fichier CSV avec pandas
    df = pd.read_csv(csv_file, encoding='utf-8-sig', delimiter=';')

    # Créer un dictionnaire pour stocker les catégories et les phrases
    categories = {}

    # Boucler sur les colonnes du DataFrame
    for column in df.columns:
        # Boucler sur les lignes de chaque colonne
        categories[column] = df[column].dropna().tolist()

    return categories
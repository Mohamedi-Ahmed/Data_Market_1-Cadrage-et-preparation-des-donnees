import pandas as pd
import os

# Chemins
input_path = os.path.join("..", "data", "decathlon_webscrapped_raw.csv")
output_path = os.path.join("..", "outputs", "products_clean.csv")

# Chargement des données
df = pd.read_csv(input_path)

# Affichage des colonnes pour debug
print("Colonnes disponibles :", df.columns.tolist())

# Suppression des doublons
df = df.drop_duplicates()

# Nettoyage : suppression des lignes sans nom ou sans prix
df = df.dropna(subset=["product_name", "sale_price"])

# Renommage des colonnes pour uniformiser
df = df.rename(columns={
    "product_url": "url",
    "product_name": "name",
    "brand": "brand",
    "star_rating": "rating",
    "number_of_reviews": "review_count",
    "MRP": "price_mrp",
    "sale_price": "price_sale",
    "product_information": "information"
})

# Nettoyage des types
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce")
df["price_mrp"] = pd.to_numeric(df["price_mrp"], errors="coerce")
df["price_sale"] = pd.to_numeric(df["price_sale"], errors="coerce")

# Export
df.to_csv(output_path, index=False)
print("Fichier nettoyé exporté vers :", output_path)
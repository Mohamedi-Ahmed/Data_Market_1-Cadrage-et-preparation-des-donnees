import pandas as pd
import sqlite3
import os

# Chemins
input_path = os.path.join("..", "outputs", "products_clean.csv")
db_path = os.path.join("..", "outputs", "data_market.db")

# Chargement
df = pd.read_csv(input_path)

# Connexion SQLite
conn = sqlite3.connect(db_path)

# Export en table
df.to_sql("products", conn, if_exists="replace", index=False)

# Fermeture
conn.close()
print("Données exportées dans la base SQLite :", db_path)
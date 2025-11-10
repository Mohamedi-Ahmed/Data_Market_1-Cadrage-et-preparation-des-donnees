import sqlite3
import pandas as pd
import os

def connect_to_db():
    db_path = os.path.join("..", "outputs", "data_market.db")
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Base de données introuvable : {db_path}")
    return sqlite3.connect(db_path)

def execute_query(conn, query, title):
    print("\n" + "=" * 80)
    print(f"{title}")
    print("=" * 80)
    print(f"\nRequête SQL :\n{query}\n")

    df = pd.read_sql_query(query, conn)
    print(f"Résultats ({len(df)} lignes) :\n")
    print(df.to_string(index=False))
    print("\n")

def main():
    print("\n" + "=" * 80)
    print("  DATA MARKET - EXEMPLES DE REQUÊTES SQL")
    print("=" * 80)

    try:
        conn = connect_to_db()

        query_top = 
        execute_query(conn, query_top, "Top 10 produits les plus populaires")

        query_promos = 
        execute_query(conn, query_promos, "Top 10 meilleures promotions")

        query_cat = 
        execute_query(conn, query_cat, "Top 10 catégories par engagement")

        query_brand = 
        execute_query(conn, query_brand, "Top 10 marques par satisfaction")

        query_gems = 
        execute_query(conn, query_gems, "Produits à mettre en avant (haute note, peu connus)")

        conn.close()

        print("\n" + "=" * 80)
        print("  TOUTES LES REQUÊTES EXÉCUTÉES AVEC SUCCÈS")
        print("=" * 80 + "\n")

    except FileNotFoundError as e:
        print(f"\nErreur : {e}")
        print("Assurez-vous d'avoir exécuté les scripts 01 et 02 d'abord.\n")
    except Exception as e:
        print(f"\nErreur : {str(e)}\n")
        raise

if __name__ == "__main__":
    main()

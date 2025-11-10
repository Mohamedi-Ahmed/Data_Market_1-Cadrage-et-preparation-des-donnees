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

    return df

def main():
    print("\n" + "=" * 80)
    print("  DATA MARKET - EXEMPLES DE REQUÊTES SQL")
    print("=" * 80)

    try:
        conn = connect_to_db()
        results = {}

        query_top = """
        SELECT
            name,
            brand,
            category,
            rating,
            review_count,
            popularity_score
        FROM view_top_products
        WHERE rating IS NOT NULL
        ORDER BY rating DESC, review_count DESC
        LIMIT 10;
        """
        results['Top_Produits'] = execute_query(conn, query_top, "Top 10 produits les plus populaires")

        query_promos = """
        SELECT
            name,
            brand,
            category,
            price_mrp,
            price_sale,
            computed_discount_pct
        FROM view_promotions
        WHERE computed_discount_pct IS NOT NULL
        ORDER BY computed_discount_pct DESC
        LIMIT 10;
        """
        results['Top_Promotions'] = execute_query(conn, query_promos, "Top 10 meilleures promotions")

        query_cat = """
        SELECT
            category,
            product_count,
            avg_rating,
            total_reviews
        FROM view_category_stats
        ORDER BY total_reviews DESC
        LIMIT 10;
        """
        results['Top_Categories'] = execute_query(conn, query_cat, "Top 10 catégories par engagement")

        query_brand = """
        SELECT
            brand,
            product_count,
            avg_rating,
            total_reviews
        FROM view_brand_stats
        WHERE avg_rating IS NOT NULL
        ORDER BY avg_rating DESC, total_reviews DESC
        LIMIT 10;
        """
        results['Top_Marques'] = execute_query(conn, query_brand, "Top 10 marques par satisfaction")

        query_gems = """
        SELECT
            name,
            brand,
            category,
            rating,
            review_count
        FROM view_top_products
        WHERE rating >= 4.5 AND review_count BETWEEN 1 AND 20
        ORDER BY rating DESC, review_count ASC
        LIMIT 10;
        """
        results['Produits_A_Mettre_En_Avant'] = execute_query(conn, query_gems, "Produits à mettre en avant (haute note, peu connus)")

        conn.close()

        excel_path = os.path.join("..", "outputs", "resultats_requetes_metier.xlsx")
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            for sheet_name, df in results.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        print("\n" + "=" * 80)
        print("  TOUTES LES REQUÊTES EXÉCUTÉES AVEC SUCCÈS")
        print(f"  Résultats exportés vers : {excel_path}")
        print("=" * 80 + "\n")

    except FileNotFoundError as e:
        print(f"\nErreur : {e}")
        print("Assurez-vous d'avoir exécuté les scripts 01 et 02 d'abord.\n")
    except Exception as e:
        print(f"\nErreur : {str(e)}\n")
        raise

if __name__ == "__main__":
    main()

import pandas as pd
import sqlite3
import os
import logging
import json
import ast

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join("..", "outputs", "database_creation.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_clean_data(input_path):
    
    try:
        logger.info(f"Chargement des données depuis {input_path}")
        df = pd.read_csv(input_path)
        logger.info(f"Données chargées : {len(df)} lignes")
        return df
    except Exception as e:
        logger.error(f"Erreur lors du chargement : {str(e)}")
        raise

def create_brands_table(df):

    brands = df[['brand']].drop_duplicates().dropna()
    brands = brands.reset_index(drop=True)
    brands['brand_id'] = range(1, len(brands) + 1)
    brands = brands[['brand_id', 'brand']]

    logger.info(f"Table brands créée : {len(brands)} marques uniques")

    return brands

def create_categories_table(df):

    categories = df[['category']].drop_duplicates().dropna()
    categories = categories.reset_index(drop=True)
    categories['category_id'] = range(1, len(categories) + 1)
    categories = categories[['category_id', 'category']]

    logger.info(f"Table categories créée : {len(categories)} catégories uniques")

    return categories

def create_products_table(df, brands_df, categories_df):

    products = df.merge(brands_df, on='brand', how='left')

    products = products.merge(categories_df, on='category', how='left')

    products['product_id'] = range(1, len(products) + 1)

    products_table = products[[
        'product_id',
        'name',
        'brand_id',
        'category_id',
        'url',
        'colour',
        'price_mrp',
        'price_sale',
        'discount_rate',
        'is_on_sale',
        'information',
        'description'
    ]].copy()

    logger.info(f"Table products créée : {len(products_table)} produits")

    return products_table, products

def create_reviews_table(products_df):
    
    reviews = products_df[[
        'product_id',
        'rating',
        'review_count',
        'popularity_score'
    ]].copy()

    reviews = reviews[reviews['review_count'].notna() & (reviews['review_count'] > 0)]

    logger.info(f"Table reviews créée : {len(reviews)} produits avec avis")

    return reviews

def parse_product_information(info_str):
    
    if pd.isna(info_str):
        return {}

    try:

        info_dict = ast.literal_eval(info_str)
        return info_dict
    except Exception:
        try:

            info_dict = json.loads(info_str)
            return info_dict
        except Exception:
            return {}

def create_product_attributes_table(products_df):
    
    attributes_list = []

    for idx, row in products_df.iterrows():
        product_id = row['product_id']
        info = parse_product_information(row['information'])

        for key, value in info.items():
            attributes_list.append({
                'product_id': product_id,
                'attribute_key': key.strip(),
                'attribute_value': str(value).strip() if value else None
            })

    attributes_df = pd.DataFrame(attributes_list)

    if len(attributes_df) > 0:
        logger.info(f"Table product_attributes créée : {len(attributes_df)} attributs")
    else:
        logger.warning("Aucun attribut extrait du champ information")

    return attributes_df

def create_database_schema(conn):
    
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    logger.info("Schéma de base de données initialisé avec contraintes")

def create_indexes(conn):
    
    cursor = conn.cursor()

    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand_id);",
        "CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);",
        "CREATE INDEX IF NOT EXISTS idx_products_price ON products(price_sale);",
        "CREATE INDEX IF NOT EXISTS idx_products_discount ON products(discount_rate);",
        "CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);",
        "CREATE INDEX IF NOT EXISTS idx_reviews_popularity ON reviews(popularity_score);",
        "CREATE INDEX IF NOT EXISTS idx_attributes_key ON product_attributes(attribute_key);"
    ]

    for index_sql in indexes:
        cursor.execute(index_sql)

    conn.commit()
    logger.info(f"{len(indexes)} index créés")

def create_business_views(conn):
    cursor = conn.cursor()

    view_catalog = """
    CREATE VIEW IF NOT EXISTS view_catalog AS
    SELECT
        p.product_id,
        p.name,
        b.brand,
        c.category,
        p.url,
        p.colour,
        p.price_mrp,
        p.price_sale,
        CASE
          WHEN p.price_sale IS NOT NULL AND p.price_sale > 0 THEN p.price_sale
          ELSE p.price_mrp
        END AS effective_price,
        CASE
          WHEN p.price_mrp IS NOT NULL AND p.price_mrp > 0
               AND p.price_sale IS NOT NULL AND p.price_sale >= 0
          THEN ROUND(100.0 * (p.price_mrp - p.price_sale) / p.price_mrp, 2)
          ELSE NULL
        END AS computed_discount_pct,
        p.discount_rate,
        p.is_on_sale
    FROM products p
    LEFT JOIN brands b ON p.brand_id = b.brand_id
    LEFT JOIN categories c ON p.category_id = c.category_id;
    """

    view_top_products = """
    CREATE VIEW IF NOT EXISTS view_top_products AS
    SELECT
        p.product_id,
        p.name,
        b.brand,
        c.category,
        r.rating,
        r.review_count,
        r.popularity_score
    FROM products p
    LEFT JOIN reviews r ON r.product_id = p.product_id
    LEFT JOIN brands b ON p.brand_id = b.brand_id
    LEFT JOIN categories c ON p.category_id = c.category_id;
    """

    view_promotions = """
    CREATE VIEW IF NOT EXISTS view_promotions AS
    SELECT *
    FROM view_catalog
    WHERE
        (price_mrp IS NOT NULL AND price_sale IS NOT NULL AND price_sale < price_mrp)
        OR (discount_rate IS NOT NULL AND discount_rate > 0)
        OR (is_on_sale = 1);
    """

    view_category_stats = """
    CREATE VIEW IF NOT EXISTS view_category_stats AS
    SELECT
        c.category,
        COUNT(p.product_id) AS product_count,
        ROUND(AVG(
            CASE
              WHEN p.price_sale IS NOT NULL AND p.price_sale > 0 THEN p.price_sale
              ELSE p.price_mrp
            END
        ), 2) AS avg_effective_price,
        ROUND(AVG(r.rating), 2) AS avg_rating,
        SUM(r.review_count) AS total_reviews,
        MIN(CASE WHEN p.price_sale IS NOT NULL AND p.price_sale > 0 THEN p.price_sale ELSE p.price_mrp END) AS min_price,
        MAX(CASE WHEN p.price_sale IS NOT NULL AND p.price_sale > 0 THEN p.price_sale ELSE p.price_mrp END) AS max_price
    FROM categories c
    LEFT JOIN products p ON p.category_id = c.category_id
    LEFT JOIN reviews r  ON r.product_id = p.product_id
    GROUP BY c.category;
    """

    view_brand_stats = """
    CREATE VIEW IF NOT EXISTS view_brand_stats AS
    SELECT
        b.brand,
        COUNT(p.product_id) AS product_count,
        ROUND(AVG(
            CASE
              WHEN p.price_sale IS NOT NULL AND p.price_sale > 0 THEN p.price_sale
              ELSE p.price_mrp
            END
        ), 2) AS avg_effective_price,
        ROUND(AVG(r.rating), 2) AS avg_rating,
        SUM(r.review_count) AS total_reviews,
        MIN(CASE WHEN p.price_sale IS NOT NULL AND p.price_sale > 0 THEN p.price_sale ELSE p.price_mrp END) AS min_price,
        MAX(CASE WHEN p.price_sale IS NOT NULL AND p.price_sale > 0 THEN p.price_sale ELSE p.price_mrp END) AS max_price
    FROM brands b
    LEFT JOIN products p ON p.brand_id = b.brand_id
    LEFT JOIN reviews r  ON r.product_id = p.product_id
    GROUP BY b.brand;
    """

    views = [
        view_catalog,
        view_top_products,
        view_promotions,
        view_category_stats,
        view_brand_stats
    ]

    for view_sql in views:
        cursor.execute(view_sql)

    conn.commit()
    logger.info(f"{len(views)} vues métier créées")

def export_to_database(brands, categories, products, reviews, attributes, db_path):
    
    try:

        if os.path.exists(db_path):
            os.remove(db_path)
            logger.info("Ancienne base de données supprimée")

        conn = sqlite3.connect(db_path)

        create_database_schema(conn)

        brands.to_sql("brands", conn, if_exists="replace", index=False)
        logger.info("Table brands exportée")

        categories.to_sql("categories", conn, if_exists="replace", index=False)
        logger.info("Table categories exportée")

        products.to_sql("products", conn, if_exists="replace", index=False)
        logger.info("Table products exportée")

        reviews.to_sql("reviews", conn, if_exists="replace", index=False)
        logger.info("Table reviews exportée")

        if len(attributes) > 0:
            attributes.to_sql("product_attributes", conn, if_exists="replace", index=False)
            logger.info("Table product_attributes exportée")

        create_indexes(conn)

        create_business_views(conn)

        conn.close()

        logger.info(f"Base de données créée avec succès : {db_path}")

    except Exception as e:
        logger.error(f"Erreur lors de la création de la base : {str(e)}")
        raise

def generate_database_stats(db_path):
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    logger.info("=" * 60)
    logger.info("STATISTIQUES DE LA BASE DE DONNÉES")
    logger.info("=" * 60)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    logger.info(f"Tables créées : {[t[0] for t in tables]}")

    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        logger.info(f"  - {table_name}: {count} lignes")

    cursor.execute("SELECT name FROM sqlite_master WHERE type='view';")
    views = cursor.fetchall()
    logger.info(f"Vues métier créées : {[v[0] for v in views]}")

    conn.close()

def main():

    input_path = os.path.join("..", "outputs", "products_clean.csv")
    db_path = os.path.join("..", "outputs", "data_market.db")

    logger.info("=" * 60)
    logger.info("DÉBUT DE LA CRÉATION DE LA BASE DE DONNÉES")
    logger.info("=" * 60)

    try:

        df = load_clean_data(input_path)

        brands = create_brands_table(df)
        categories = create_categories_table(df)
        products, products_full = create_products_table(df, brands, categories)
        reviews = create_reviews_table(products_full)
        attributes = create_product_attributes_table(products_full)

        export_to_database(brands, categories, products, reviews, attributes, db_path)

        generate_database_stats(db_path)

        logger.info("=" * 60)
        logger.info("BASE DE DONNÉES CRÉÉE AVEC SUCCÈS")
        logger.info("=" * 60)

    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"ÉCHEC DE LA CRÉATION : {str(e)}")
        logger.error("=" * 60)
        raise

if __name__ == "__main__":
    main()
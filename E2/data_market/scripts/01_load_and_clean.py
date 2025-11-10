import pandas as pd
import numpy as np
import os
import logging
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join("..", "outputs", "data_processing.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_data(input_path):
    try:
        logger.info(f"Chargement des données depuis {input_path}")
        df = pd.read_csv(input_path)
        logger.info(f"Données chargées avec succès : {len(df)} lignes, {len(df.columns)} colonnes")
        logger.info(f"Colonnes disponibles : {df.columns.tolist()}")
        return df
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {input_path}")
        raise
    except pd.errors.EmptyDataError:
        logger.error(f"Fichier vide : {input_path}")
        raise
    except Exception as e:
        logger.error(f"Erreur lors du chargement : {str(e)}")
        raise


def remove_duplicates(df):
    initial_count = len(df)
    df = df.drop_duplicates()
    duplicates_removed = initial_count - len(df)

    if duplicates_removed > 0:
        logger.warning(f"{duplicates_removed} doublons supprimés")
    else:
        logger.info("Aucun doublon détecté")

    return df


def clean_missing_values(df):
    initial_count = len(df)
    df = df.dropna(subset=["product_name", "sale_price"])

    missing_removed = initial_count - len(df)
    if missing_removed > 0:
        logger.warning(f"{missing_removed} lignes supprimées (valeurs manquantes critiques)")

    missing_summary = df.isnull().sum()
    missing_summary = missing_summary[missing_summary > 0]

    if len(missing_summary) > 0:
        logger.info("Valeurs manquantes par colonne :")
        for col, count in missing_summary.items():
            logger.info(f"  - {col}: {count} ({count/len(df)*100:.1f}%)")

    return df


def rename_columns(df):
    column_mapping = {
        "product_url": "url",
        "product_name": "name",
        "brand": "brand",
        "star_rating": "rating",
        "number_of_reviews": "review_count",
        "MRP": "price_mrp",
        "sale_price": "price_sale",
        "colour": "colour",
        "product information": "information",
        "description": "description"
    }

    df = df.rename(columns=column_mapping)
    logger.info("Colonnes renommées avec succès")

    return df


def convert_data_types(df):
    numeric_columns = ["rating", "review_count", "price_mrp", "price_sale"]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            invalid_count = df[col].isnull().sum()
            if invalid_count > 0:
                logger.warning(f"{col}: {invalid_count} valeurs invalides converties en NaN")

    logger.info("Conversion des types de données terminée")

    return df


def extract_category_from_url(url):
    if pd.isna(url):
        return "Unknown"

    try:
        match = re.search(r'/products/([^/]+)', url)
        if match:
            product_slug = match.group(1)
            parts = product_slug.split('-')
            if 'womens' in parts or 'mens' in parts:
                return parts[1] if len(parts) > 1 else "Unknown"
            return parts[0] if parts else "Unknown"
    except Exception:
        return "Unknown"

    return "Unknown"


def add_calculated_fields(df):
    df["discount_rate"] = np.where(
        (df["price_mrp"].notna()) & (df["price_mrp"] > 0),
        ((df["price_mrp"] - df["price_sale"]) / df["price_mrp"] * 100).round(2),
        0.0
    )

    df["is_on_sale"] = df["discount_rate"] > 0
    df["category"] = df["url"].apply(extract_category_from_url)
    df["popularity_score"] = np.where(
        df["review_count"].notna() & df["rating"].notna(),
        (df["rating"] * np.log1p(df["review_count"])).round(2),
        0.0
    )

    logger.info("Champs calculés ajoutés : discount_rate, is_on_sale, category, popularity_score")

    return df


def validate_data(df):
    issues = []

    if (df["price_sale"] < 0).any():
        issues.append("Détection de prix de vente négatifs")

    if ((df["rating"] < 0) | (df["rating"] > 5)).any():
        issues.append("Détection de ratings invalides (< 0 ou > 5)")

    if (df["review_count"] < 0).any():
        issues.append("Détection de nombres d'avis négatifs")
    incoherent_prices = df[df["price_sale"] > df["price_mrp"]].shape[0]
    if incoherent_prices > 0:
        issues.append(f"{incoherent_prices} produits avec prix soldé > prix catalogue")

    if issues:
        logger.warning("Problèmes de validation détectés :")
        for issue in issues:
            logger.warning(f"  - {issue}")
        return False
    else:
        logger.info("Validation des données réussie")
        return True


def export_data(df, output_path):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info(f"Données exportées avec succès vers {output_path}")
        logger.info(f"Fichier final : {len(df)} lignes, {len(df.columns)} colonnes")
    except Exception as e:
        logger.error(f"Erreur lors de l'export : {str(e)}")
        raise


def main():
    input_path = os.path.join("..", "data", "decathlon_webscrapped_raw.csv")
    output_path = os.path.join("..", "outputs", "products_clean.csv")

    logger.info("=" * 60)
    logger.info("DÉBUT DU TRAITEMENT")
    logger.info("=" * 60)

    try:
        df = load_data(input_path)
        df = remove_duplicates(df)
        df = clean_missing_values(df)
        df = rename_columns(df)
        df = convert_data_types(df)
        df = add_calculated_fields(df)
        validate_data(df)
        export_data(df, output_path)

        logger.info("=" * 60)
        logger.info("TRAITEMENT TERMINÉ AVEC SUCCÈS")
        logger.info("=" * 60)

    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"ÉCHEC DU TRAITEMENT : {str(e)}")
        logger.error("=" * 60)
        raise


if __name__ == "__main__":
    main()
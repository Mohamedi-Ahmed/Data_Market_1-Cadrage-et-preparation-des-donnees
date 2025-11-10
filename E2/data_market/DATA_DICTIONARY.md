# Data Dictionary - Base de données Data Market

Documentation du modèle de données `data_market.db`.

---

## Modèle relationnel

```text
brands ──┐
         ├──> products ──┬──> reviews
categories ─┘            └──> product_attributes
```

---

## Tables

### 1. `brands`

Référentiel des marques.

| Colonne     | Type    | Description                          |
|-------------|---------|--------------------------------------|
| `brand_id`  | INTEGER | Identifiant unique de la marque (PK) |
| `brand`     | TEXT    | Nom de la marque                     |

**Volumétrie** : ~22 marques

---

### 2. `categories`

Référentiel des catégories extraites des URLs.

| Colonne        | Type    | Description                              |
|----------------|---------|------------------------------------------|
| `category_id`  | INTEGER | Identifiant unique de la catégorie (PK)  |
| `category`     | TEXT    | Nom de la catégorie                      |

**Volumétrie** : ~182 catégories

**Note** : L'extraction des catégories est basique et mériterait d'être améliorée avec un mapping manuel.

---

### 3. `products`

Table principale des produits.

| Colonne         | Type    | Description                                      |
|-----------------|---------|--------------------------------------------------|
| `product_id`    | INTEGER | Identifiant unique du produit (PK)               |
| `name`          | TEXT    | Nom du produit                                   |
| `brand_id`      | INTEGER | Référence vers brands (FK)                       |
| `category_id`   | INTEGER | Référence vers categories (FK)                   |
| `url`           | TEXT    | URL du produit                                   |
| `colour`        | TEXT    | Couleur                                          |
| `price_mrp`     | FLOAT   | Prix catalogue USD                               |
| `price_sale`    | FLOAT   | Prix de vente USD                                |
| `discount_rate` | FLOAT   | Taux de remise %                                 |
| `is_on_sale`    | BOOLEAN | Indicateur promotion                             |
| `information`   | TEXT    | Informations techniques (JSON)                   |
| `description`   | TEXT    | Description marketing                            |

**Volumétrie** : 639 produits

---

### 4. `reviews`

Avis clients agrégés par produit.

| Colonne            | Type    | Description                               |
|--------------------|---------|-------------------------------------------|
| `product_id`       | INTEGER | Référence vers products (FK)              |
| `rating`           | FLOAT   | Note moyenne (0-5)                        |
| `review_count`     | INTEGER | Nombre d'avis                             |
| `popularity_score` | FLOAT   | Score : rating × ln(review_count + 1)     |

---

### 5. `product_attributes`

Attributs techniques extraits du JSON.

| Colonne           | Type    | Description                              |
|-------------------|---------|------------------------------------------|
| `product_id`      | INTEGER | Référence vers products (FK)             |
| `attribute_key`   | TEXT    | Nom de l'attribut                        |
| `attribute_value` | TEXT    | Valeur                                   |

**Volumétrie** : 4396 attributs

---

## Vues métier

### `v_catalog_full`

Catalogue complet avec jointures (produits, marques, catégories, avis).

**Utilité** : Vue globale pour exports et dashboards.

---

### `v_top_products`

Produits triés par popularité.

**Utilité** : Identifier les best-sellers.

---

### `v_promotions`

Produits en promotion triés par taux de remise.

**Utilité** : Analyse des promotions.

---

### `v_category_stats`

Statistiques agrégées par catégorie.

**Colonnes** : category, product_count, avg_price, avg_rating, total_reviews, avg_discount

---

### `v_brand_stats`

Statistiques agrégées par marque.

**Colonnes** : brand, product_count, avg_price, avg_rating, total_reviews, avg_discount

---

## Exemples de requêtes SQL

### Top 10 produits populaires

```sql
SELECT name, brand, price_sale, rating, popularity_score
FROM v_top_products
LIMIT 10;
```

### Promotions > 20%

```sql
SELECT name, brand, price_mrp, price_sale, discount_rate
FROM v_promotions
WHERE discount_rate > 20
LIMIT 15;
```

### Statistiques par catégorie

```sql
SELECT * FROM v_category_stats;
```

---

**Version** : 1.0
**Date** : 2025-07-11

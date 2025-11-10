# Data Market – Étape E2 : Collecte, nettoyage et préparation des données

## Objectif

Transformer les données brutes du dataset Decathlon (Kaggle) en une base de données relationnelle propre, normalisée et documentée, prête à être exploitée par les équipes métier (Produit, Marketing, BI).

Ce projet constitue la **couche silver/gold** du Data Market, avec des données nettoyées, enrichies et structurées pour faciliter les analyses.

---

## Démarrage

```bash
# 1. Installation des dépendances
pip install -r ../../requirements.txt

# 2. Exécution du pipeline complet
cd E2/data_market/scripts

python 01_load_and_clean.py
python 02_split_tables.py
python 03_business_queries.py

# 3. Résultats disponibles dans E2/data_market/outputs/
```

---

## Structure du projet

```text
/data_market/
│
├── data/                              # Données brutes
│   └── decathlon_webscrapped_raw.csv  (639 produits Decathlon)
│
├── scripts/                           # Pipeline de traitement
│   ├── 01_load_and_clean.py          Script de nettoyage et enrichissement
│   ├── 02_split_tables.py            Script de normalisation BDD
│   └── 03_business_queries.py        Exemples de requêtes métier
│
├── outputs/                           # Résultats générés
│   ├── products_clean.csv            CSV nettoyé et enrichi
│   ├── data_market.db                Base SQLite normalisée
│   ├── resultats_requetes_metier.xlsx Résultats des requêtes SQL (Excel)
│   ├── data_processing.log           Log du nettoyage
│   └── database_creation.log         Log de la création BDD
│
├── DATA_DICTIONARY.md                 Documentation complète du modèle
└── README.md                          Documentation technique (ce fichier)
```

---

## Scripts fournis

### `01_load_and_clean.py`

Nettoyage et enrichissement des données : suppression doublons, gestion valeurs manquantes, conversion types, extraction catégories depuis URL, calcul de métriques (`discount_rate`, `is_on_sale`, `popularity_score`).

### `02_split_tables.py`

Normalisation de la base de données relationnelle : création de 5 tables (`brands`, `categories`, `products`, `reviews`, `product_attributes`), index et 5 vues métier pour analyses.

**Modèle relationnel (3NF)** :

```text
brands ──┐
         ├──> products ──┬──> reviews
categories ─┘            └──> product_attributes
```

**Pourquoi 3NF et pas un schéma en étoile ?**

Le modèle relationnel normalisé (3NF) a été choisi car ce projet vise à préparer des données propres et réutilisables, pas à créer un data warehouse pour de l'analytique temps réel. Un schéma en étoile (fact/dimensions) serait pertinent avec des données de ventes historisées et des millions de lignes nécessitant des agrégations rapides. Ici, avec 639 produits statiques, la normalisation permet plus de flexibilité pour des requêtes variées tout en éliminant les redondances.

### `03_business_queries.py`

Exemples de requêtes SQL métier : top produits, promotions, statistiques par catégorie/marque, produits à mettre en avant.

**Résultats exportés** : fichier Excel `resultats_requetes_metier.xlsx` avec 5 onglets (Top_Produits, Top_Promotions, Top_Categories, Top_Marques, Produits_A_Mettre_En_Avant)

---

## Prérequis

- **Python 3.8+**
- **Dépendances** : pandas, numpy, openpyxl, sqlalchemy (voir [requirements.txt](../../requirements.txt))

---

## Source de données

**Dataset Decathlon Web Scraped** (Kaggle) : 639 produits avec prix, avis clients, attributs techniques.

Lien : [https://www.kaggle.com/datasets/nikhilchadha1537/decathlon-web-scraped](https://www.kaggle.com/datasets/nikhilchadha1537/decathlon-web-scraped)

**Qualité** : 0 doublons, 100% de complétude sur champs critiques, validation prix/ratings

---

## Limites et perspectives

**Limites** : source unique (Decathlon), données statiques (pas d'historique), catégories simplifiées.

**Évolutions** : ajout sources internes (commandes, stock), historisation (SCD Type 2), pipeline automatisé (Airflow), monitoring qualité (Great Expectations)


# Data Market – Étape E2 : Collecte et nettoyage

## Objectif

Transformer les données brutes du fichier `decathlon_raw.csv` (dataset Kaggle) en une structure exploitable pour le Data Market interne : nettoyage, normalisation et export.

## Structure du projet

```
/data_market/
│
├── data/                     # Fichier brut
│   └── decathlon_raw.csv
│
├── scripts/                  # Scripts de traitement
│   ├── load_and_clean.py
│   └── split_tables.py
│
├── output/                   # Résultats
│   ├── products_clean.csv
│   └── data_market.db
│
└── README.md                 # Documentation technique
```

## Scripts fournis

### `load_and_clean.py`

- Charge le fichier brut
- Supprime les doublons
- Nettoie les colonnes et descriptions
- Vérifie les types et les données manquantes
- Sauvegarde un fichier `products_clean.csv` dans `output/`

### `split_tables.py`

- Charge `products_clean.csv`
- Crée une base SQLite `data_market.db`
- Exporte la table `products` dans la base

## Prérequis

- Python 3.8+
- Pandas
- SQLite3 (intégré à Python)

Installer les dépendances :

```bash
pip install pandas
```

## Exécution

1. Placer `decathlon_raw.csv` dans `/data/`
2. Lancer les scripts :

```bash
python scripts/load_and_clean.py
python scripts/split_tables.py
```

3. Vérifier les fichiers générés dans `/output/`

## Limites

- Les avis clients ne sont pas séparés à ce stade
- Les catégories sont plates (pas d’arbre hiérarchique)
- Pas de données clients ou commandes intégrées encore

## Étapes suivantes

- Création de vues SQL pour analystes
- Croisement avec d’autres sources internes
- Enrichissement via OpenFoodFacts ou d'autres APIs


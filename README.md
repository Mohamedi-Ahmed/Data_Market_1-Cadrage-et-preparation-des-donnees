# Data Market - Cadrage et préparation des données

Projet de création d'un Data Market interne pour une entreprise e-commerce, en charge de la première phase : identification des sources, collecte, nettoyage et préparation des données.

---

## Vue d'ensemble

Ce projet est structuré en deux étapes principales :

- **E1** : Cadrage fonctionnel et cartographie des sources
- **E2** : Collecte, nettoyage et préparation des données

---

## Structure du projet

```text
Data_Market_1-Cadrage-et-preparation-des-donnees/
│
├── E1/                                   # Étape 1 : Cadrage
│   └── DataMarket_E1.md                  Note de cadrage fonctionnel
│
├── E2/                                   # Étape 2 : Collecte et nettoyage
│   └── data_market/
│       ├── data/                         Données brutes
│       ├── scripts/                      Scripts Python
│       ├── outputs/                      Résultats (CSV, DB, logs)
│       ├── DATA_DICTIONARY.md            Documentation du modèle de données
│       └── README.md                     Documentation technique détaillée
│
├── requirements.txt                      Dépendances Python
├── .gitignore                            Fichiers à exclure de Git
└── README.md                             Ce fichier
```

---

## Démarrage rapide

### 1. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 2. Exécution du pipeline complet

```bash
cd E2/data_market/scripts

# Nettoyage et enrichissement
python 01_load_and_clean.py

# Création de la base de données normalisée
python 02_split_tables.py

# Exemples de requêtes métier (optionnel)
python 03_business_queries.py
```

### 3. Résultats

Les résultats sont générés dans `E2/data_market/outputs/` :

- `products_clean.csv` : données nettoyées (format CSV)
- `data_market.db` : base de données SQLite normalisée
- `*.log` : logs de traitement

---

## Livrables du projet

### E1 : Cadrage fonctionnel

**Fichier** : [E1/DataMarket_E1.md](E1/DataMarket_E1.md)

**Contenu** :

- Contexte et objectifs du projet
- Cas d'usage métier identifiés
- Publics cibles et contraintes
- Organigramme organisationnel
- **Cartographie des sources de données**
- Synthèses d'entretiens métiers (2 profils)

---

### E2 : Collecte et nettoyage

**Documentation principale** : [E2/README.md](E2/README.md)

**Scripts fournis** :

1. **01_load_and_clean.py** : nettoyage, enrichissement, validation
2. **02_split_tables.py** : normalisation et création BDD relationnelle
3. **03_business_queries.py** : 20+ requêtes SQL métier

**Documentation** :

- [DATA_DICTIONARY.md](E2/data_market/DATA_DICTIONARY.md) : modèle de données complet

**Base de données créée** :

- 5 tables : `brands`, `categories`, `products`, `reviews`, `product_attributes`
- 5 vues métier : `v_catalog_full`, `v_top_products`, `v_promotions`, etc.
- Index et contraintes de clés étrangères

---

## Technologies utilisées

- **Langage** : Python 3.8+
- **Bibliothèques** : Pandas, NumPy, SQLAlchemy
- **Base de données** : SQLite
- **Versionning** : Git
- **Documentation** : Markdown

---

## Cas d'usage métier couverts

| Cas d'usage                       | Implémentation                          | Statut |
|-----------------------------------|-----------------------------------------|--------|
| Suivi des ventes par catégorie    | Vue `v_category_stats`                  | ✅      |
| Analyse satisfaction client       | Table `reviews` + `v_top_products`      | ✅      |
| Segmentation produits             | Requêtes SQL sur `v_catalog_full`       | ✅      |
| Benchmark produits / pricing      | Vues `v_brand_stats`, `v_promotions`    | ✅      |

---

## Limites et perspectives

### Limites actuelles

- **Source unique** : uniquement dataset Decathlon (pas de données internes commandes/clients)
- **Données statiques** : snapshot unique sans historique temporel
- **Catégories simplifiées** : extraction basique depuis URLs

### Évolutions futures recommandées

- [ ] Intégration de sources internes (commandes, clients, stock)
- [ ] Enrichissement avec APIs externes (météo, tendances, OpenFoodFacts)
- [ ] Historisation des données (SCD Type 2)
- [ ] Pipeline ETL automatisé (Airflow/Prefect)
- [ ] Monitoring qualité des données (Great Expectations)
- [ ] API REST pour exposition des données

---

## Contact

**Auteur** : Data Engineering Team
**Date** : Juillet 2025
**Formation** : Data Engineer

---

## Licence

Ce projet est réalisé dans un cadre pédagogique.

---

**Version** : 2.0
**Statut** : Production-ready ✅

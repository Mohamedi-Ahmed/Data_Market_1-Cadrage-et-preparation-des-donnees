# Data Market — Étape E1 : Cadrage et préparation des données

## 1. Contexte et objectifs

Dans le cadre de la création d’un Data Market interne pour une entreprise e-commerce, l’objectif est de structurer une première couche de données propre (stack silver voire gold) , fiable et exploitable, à destination d’équipes non techniques (Produit, Marketing, SAV)

En tant que Data Engineer junior, je dois identifier les sources pertinentes, collecter les données, les nettoyer et les structurer pour qu’elles puissent être utilisées facilement par les équipes métier dans des outils d’analyse.

---

## 2. Cadrage fonctionnel

### Cas d’usage ciblés

- Suivi des ventes par catégorie ou canal
- Analyse de la satisfaction client via les avis
- Segmentation client (fidèles, récents, churn)
- Benchmark produits / enrichissement via données publiques

### Publics concernés

- Équipes Produit : suivi des produits performants
- Marketing : ciblage et segmentation
- Data / BI : création de dashboards
- SAV / Qualité : suivi des retours

### Contraintes identifiées

- Données dispersées (fichiers, scraping, APIs)
- Nettoyage nécessaire (doublons, formats incohérents)
- Nécessité d’anonymiser les données clients
- Fréquence de mise à jour variable selon les sources

### Organigramme

```
                               PDG
                                │
                    ┌───────────┴───────────┐
                    │                       │
           Direction Produit        Direction Technique
                    │                       │
        ┌───────────┘                       └────────────┐
        │                                               │
  Équipe Produit (PO, PM)                          Équipe Data / IT
        │                                               │
        │                                  ┌────────────┴────────────┐
        │                                  │                         │
 Utilisateurs Métier                  Data Analysts            Data Engineers
 (Marketing, Finance, etc.)  
        │                                                  │
        └─────────────────────────────┬────────────────────┘
                                      │
                                  Data Market 
```

---

## 3. Cartographie des sources

| Source                         | Origine | Format         | Utilité principale           |
| ------------------------------ | ------- | -------------- | ----------------------------- |
| Commandes e-commerce           | Interne | CSV / SQL      | Suivi des ventes, CA          |
| Clients                        | Interne | CSV / SQL      | Segmentation, historique      |
| Catalogue produits (Decathlon) | Externe | CSV (Kaggle)   | Description, prix, catégorie |
| Avis clients                   | Mixte   | CSV / scraping | Note moyenne, retour client   |

---

## 4. Rôles et accès

| Rôle                     | Accès recommandé        | Données clés     |
| ------------------------- | ------------------------- | ------------------ |
| Chef de produit           | Lecture complète produit | Ventes, avis       |
| Marketing / CRM           | Lecture filtrée clients  | Profils, paniers   |
| Analyste / BI / Data Eng. | Accès complet            | Toutes les sources |
| SAV / Qualité            | Lecture partielle         | Retours, avis      |

---

## 5. Synthèse des échanges métiers

 Rôle interrogé : Responsable Produit / Développeur CMS
 Fonction : Gestion du catalogue produit / Back-office
 Date de l’entretien : 11/07/2025
 Interrogé par : Ahmed Mohamedi

| **Question posée**                                                            | **Réponse / Notes**                                           |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| Quelles données gérez-vous ou produisez-vous ?                                     | Nom du produit, catégorie, prix, image, description, stock          |
| Quels outils utilisez-vous pour cela ?                                               | CMS maison, saisie manuelle via formulaire, parfois Excel            |
| Avez-vous des règles ou validations automatiques ?                                  | Peu de règles ; certains champs sont requis mais sans vérification |
| Rencontrez-vous des problèmes fréquents avec ces données ?                        | Oui : doublons, libellés incohérents, images manquantes            |
| Avez-vous des contraintes particulières (RGPD, confidentialité, etc.) ?            | Pas sur les produits, mais oui sur certains avis clients             |
| Souhaiteriez-vous avoir un retour d’usage ou un suivi automatisé de vos données ? | Oui, notamment savoir quels produits sont les plus vus ou vendus     |

---

 Rôle interrogé : Analyste Marketing / Responsable E-commerce
 Fonction : Analyse des ventes / Optimisation de l’offre
 Date de l’entretien: 11/07/2025
 Interrogé par : Ahmed Mohamedi

| **Question posée**                                                                | **Réponse / Notes**                                             |
| ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Quels types d’analyses ou reportings réalisez-vous régulièrement ?                   | Suivi des ventes, analyse des performances produits, promo             |
| Quelles données utilisez-vous principalement ?                                          | Prix, stock, ventes, avis clients, catégorie, saisonnalité           |
| Où trouvez-vous ces données actuellement ?                                             | Base SQL via Data Team, parfois Excel exporté manuellement            |
| Rencontrez-vous des limites ou des difficultés d’accès ?                              | Oui, dépendance à l’équipe data, lenteur de réponse               |
| Dans quel format préférez-vous consulter les données ?                                | Tableaux exportables, dashboards, parfois Excel                        |
| Souhaitez-vous enrichir ces données avec d’autres sources (Open Data, météo, etc.) ? | Oui, notamment météo / événementiel pour mieux prévoir la demande |
| Aimeriez-vous accéder à ces données de manière autonome ?                            | Oui, avec filtres simples et données à jour                          |

---

Les échanges ont permis de confirmer que :

- Les données sont dispersées et souvent peu fiables
- Les équipes aimeraient croiser plusieurs sources (ventes + avis + stock)
- Les profils non techniques veulent un accès simple (fichiers excel ou vues BI)
- Des enrichissements externes sont bienvenus si pertinents

 # Journal de Décision Data — Projet Recommandation Livres (Creuse)

## Table : `livres_auteurs.csv`
**Responsable :** [Prénom à renseigner] | **Date :** 17/11/2026 | **Sprint :** Sprint 2 (Préparation & Nettoyage)

---

### Décision #01 : Suppression des doublons sur le couple `(work_id, author_id)`
- **Constat (audit initial) :**
	- Volume initial : `63 412` lignes (`48 766` œuvres uniques, `31 373` auteurs uniques).
	- `[50]` lignes en doublon sur la clé composite `(work_id, author_id)` : un même auteur peut être associé plusieurs fois à la même œuvre avec des valeurs d’`ordre` différentes.
- **Risque métier / algorithmique :**
	- Biais dans le calcul des auteurs les plus prolifiques (surcomptage artificiel).
	- Fausse pondération de la similarité par auteur dans le moteur de recommandation (*cold start*).
- **Règle de gestion retenue :**
	1. Trier par `ordre` croissant (`ascending=True`).
	2. Dédupliquer sur `(work_id, author_id)` en conservant la première occurrence (`keep='first'`), soit le rang d’attribution le plus élevé.
- **Impact quantitatif :**
	- Lignes supprimées : `[25]` (`[0.04 %]` du volume initial).
	- Volume final nettoyé (`livres_auteurs_clean.csv`) : `[63 412 - 25]` lignes.
	- Intégrité référentielle : vérifier après nettoyage que les `48 766` œuvres et `31 373` auteurs restent couverts à 100 %.
	- Les valeurs entre crochets sont à renseigner après exécution du nettoyage et contrôle des données.

---

### Décision #02 : Conservation de la colonne `ordre` (auteur principal vs co-auteurs)
- **Constat :** La colonne `ordre` varie de `1` à `237` (ouvrages collectifs / anthologies).
- **Règle de gestion retenue :** Conserver toutes les associations dédupliquées dans la table de liaison. Utiliser le filtre `ordre == 1` pour l’analyse exploratoire des auteurs principaux et une pondération décroissante selon `ordre` dans l’algorithme de recommandation.

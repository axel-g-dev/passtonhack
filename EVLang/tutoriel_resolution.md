Voici la solution détaillée étape par étape.

### 1. Reconstitution de la Grille

D'après le code Javascript fourni (`loadInstruction`), voici à quoi ressemble la grille du programme (9 colonnes x 5 lignes). J'ai simplifié les symboles pour la lisibilité :

|  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **0** | `➡️` | `🥞30` | `🥞6` | `🥞39` | `🥞-2` | `⬇️` |  |  | `💸` |
| **1** | `🏁` | `⬇️` | `🥞-16` | `🥞-10` | `🥞33` | `⬅️` | `⬇️` | `🈶` | `🎰` |
| **2** |  |  |  | `↘️` | `🥞-67` | `⏩` | `⬅️` |  |  |
| **3** |  | `⬅️` |  |  | `➡️` | `➕` | `⚖️` | `⬇️` | `⬆️` |
| **4** |  |  |  |  |  |  | `🚫` | `🎰` | `⬇️` |

### 2. Trace de l'Exécution

Suivons le chemin du curseur pour voir comment la pile se remplit.

**Phase 1 : Initialisation (Ligne 0)**

* Le curseur part en `0,0` vers la droite.
* Il empile successivement : **30, 6, 39, -2**.
* **Pile :** `[30, 6, 39, -2]` (Le -2 est au sommet).
* En `0,5`, la flèche `⬇️` envoie le curseur vers le bas.

**Phase 2 : Le virage (Ligne 1)**

* Le curseur arrive en `1,5` où il rencontre `⬅️`. Il part à gauche.
* Il empile successivement : **33, -10, -16**.
* **Pile complète :** `[30, 6, 39, -2, 33, -10, -16]` (Le -16 est au sommet).
* En `1,1`, la flèche `⬇️` l'envoie vers le bas.

**Phase 3 : L'entrée dans la boucle (Navigation)**

* Le curseur descend, traverse des cases vides, suit des flèches (`⬅️` en 3,1, puis remonte via `⬆️` en 3,8).
* Il finit par atterrir sur la case clé en **1,8** : le Branch `🎰`.

**Phase 4 : La Boucle de Vérification**
C'est ici que tout se joue. L'instruction `🎰` regarde le sommet de la pile.

* Si le sommet est **0** (ou vide) : On va à Droite (vers la Victoire `🏁`).
* Si le sommet **n'est pas 0** : On va à Gauche (vers la vérification).

Au premier passage, le sommet est `-16`. On va donc à gauche pour vérifier le caractère.

**L'algorithme de vérification (Le "Crackme") :**

1. `🈶` (1,7) : Prend le caractère actuel du mot de passe (ex: 'X') et le met sur la pile.
2. `⏩` (2,5) : Avance le pointeur mémoire au caractère suivant.
3. `🥞-67` (2,4) : Empile -67.
4. `➕` (3,5) : Additionne les deux derniers (`Caractère + (-67)`).
5. `⚖️` (3,6) : Compare le résultat avec la valeur cible qui était sur la pile.
* Le calcul est : `(Caractère - 67) == Valeur_Cible`
* Donc : **`Caractère = Valeur_Cible + 67`**



Si la comparaison est bonne, le résultat est `0`. Le `Branch` suivant (4,7) nous envoie faire une boucle qui retire ce `0` et nous ramène au `Branch` principal (1,8) pour tester la valeur suivante de la pile.

### 3. Décodage du Mot de Passe

La pile fonctionne en LIFO (Dernier entré, premier sorti). Nous devons dépiler les valeurs dans l'ordre inverse de leur insertion pour trouver les caractères.

La pile contient (du bas vers le haut) : `30, 6, 39, -2, 33, -10, -16`.

| Ordre de sortie | Valeur Cible | Calcul (Cible + 67) | Code ASCII | Caractère |
| --- | --- | --- | --- | --- |
| **1** (Sommet) | -16 | -16 + 67 = 51 | 51 | **3** |
| **2** | -10 | -10 + 67 = 57 | 57 | **9** |
| **3** | 33 | 33 + 67 = 100 | 100 | **d** |
| **4** | -2 | -2 + 67 = 65 | 65 | **A** |
| **5** | 39 | 39 + 67 = 106 | 106 | **j** |
| **6** | 6 | 6 + 67 = 73 | 73 | **I** |
| **7** (Fond) | 30 | 30 + 67 = 97 | 97 | **a** |

Une fois la pile vide, l'instruction `🎰` voit que la pile est vide et va à Droite, ce qui mène au drapeau `🏁`.

### Solution

Le mot de passe est la concaténation des caractères trouvés : **39dAjIa**

Le format demandé est :
`FLAG{39dAjIa}`
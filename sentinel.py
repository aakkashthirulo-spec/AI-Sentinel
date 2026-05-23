import time
import os

from utils.parser import charger_logs
from utils.stats import calculer_zscores

from detection.flood import detecter_flood
from detection.injection import detecter_injections
from detection.brute_force import detecter_brute_force
from detection.scan_ports import detecter_scan_ports

from termcolor import colored, cprint

import sys

# =====================================================
# CONFIGURATION
# =====================================================

SEUIL_ZSCORE = 2.5
#PAYS_SUSPECTS = ["RUSSIE", "CHINE", "COREE DU NORD"]
PAYS_SUSPECTS = ["RU", "CN", "KP", "BR"]

# =====================================================
# ANALYSE D'UN LOG
# =====================================================

def analyser_log(log, scores_z, i, score_risque, menaces):
    # PAYLOAD ANORMAL - ROUGE
    try:
        taille_payload = float(log['payload_num'])
    except (ValueError, KeyError):
        taille_payload = 0

    if abs(scores_z[i]) > SEUIL_ZSCORE:
        print(colored(f"PAYLOAD ANORMAL ({log['payload_num']})", "red", attrs=["bold"]))
        score_risque += 20
        if "Payload Anormal" not in menaces:
            menaces.append("Payload Anormal")

    # ACTIVITÉ SUSPECTE - MAGENTA
    try:
        heure_log = int(log['heure'])
    except (ValueError, KeyError):
        heure_log = 12

    if not (8 <= heure_log <= 18):
        print(colored(f"ACTIVITÉ SUSPECTE ({heure_log}h)", "magenta", attrs=["bold"]))
        score_risque += 5

    # PAYS SUSPECT - MAGENTA
    if log.get('pays', '').upper() in PAYS_SUSPECTS:
        print(colored(f"PAYS SUSPECT : {log['pays']}", "magenta", attrs=["bold"]))
        score_risque += 10

    return score_risque, menaces

# =====================================================
# ANALYSE PRINCIPALE
# =====================================================

def analyser_systeme(chemin_fichier, ip):
    donnees = charger_logs(chemin_fichier)

    if not donnees:
        cprint("Aucun log disponible", "red", attrs=["bold"])
        return

    # Adaptation au nouveau nom de colonne 'payload_num' pour le Z-score
    tailles = []
    for d in donnees:
        try:
            tailles.append(float(d['payload_num']))
        except (ValueError, KeyError):
            tailles.append(0)

    scores_z = calculer_zscores(tailles)

    score_risque = 0
    menaces = []

    # =====================================================
    # HEADER
    # =====================================================

    os.system("cls" if os.name == "nt" else "clear")

    cprint("===================================", "cyan", attrs=["bold"])
    cprint("        AI-SENTINEL — LIVE MODE", "cyan", attrs=["bold"])
    cprint("===================================", "cyan", attrs=["bold"])

    print(colored(f"[SCAN INITIÉ] CIBLE : {ip}", "cyan", attrs=["bold"]))

    # =====================================================
    # PRE-CHECK GLOBAL
    # =====================================================

    flood, _ = detecter_flood(donnees, ip)
    scan, _ = detecter_scan_ports(donnees, ip)
    brute, _ = detecter_brute_force(donnees, ip)
    injections = detecter_injections(donnees, ip)

    if flood:
        print(colored(" FLOOD DÉTECTÉ", "red", attrs=["bold"]))
        score_risque += 30
        menaces.append("Flood")

    if scan:
        print(colored(" PORT SCANNING DÉTECTÉ", "red", attrs=["bold"]))
        score_risque += 20
        menaces.append("Port Scanning")

    if brute:
        print(colored(" BRUTE FORCE DÉTECTÉ", "red", attrs=["bold"]))
        score_risque += 40
        menaces.append("Brute Force")

    if injections:
        for inj in injections:
            print(colored(inj, "red", attrs=["bold"]))
            score_risque += 25
        menaces.append("Injection")

    print(colored("\n[LIVE STREAM ACTIVÉ]\n", "cyan", attrs=["bold"]))

    # =====================================================
    # LIVE MODE
    # =====================================================

    for i, log in enumerate(donnees):

        if log['ip_source'] != ip:
            continue

        # LOGS
        
        print(colored(f"[LOG] {log['heure']} | {log['ip_source']} | {log['port']} | {log['pays']} | {log['payload_num']}", "cyan"))
        
        score_risque, menaces = analyser_log(log,scores_z,i,score_risque,menaces)

        time.sleep(0.5)

    # =====================================================
    # VERDICT FINAL
    # =====================================================

    print("\n===================================")

    if score_risque < 40:
        niveau = "FAIBLE"
        couleur = "yellow"
    elif score_risque < 80:
        niveau = "MOYEN"
        couleur = "magenta"
    else:
        niveau = "CRITIQUE"
        couleur = "red"

    print(colored(f" SCORE DE RISQUE : {score_risque}","red",attrs=["bold"]))

    print(colored(f" NIVEAU : {niveau}",couleur,attrs=["bold"]))

    # =====================================================
    # MENACES
    # =====================================================

    if menaces:
        print(colored("\n  MENACES DÉTECTÉES :", "red", attrs=["bold"]))
        for m in set(menaces):
            print(colored(f" - {m}", "red"))
    else:
        print(colored("\n Aucune menace détectée", "green", attrs=["bold"]))

    print(colored("===================================\n", "cyan", attrs=["bold"]))


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    cprint("===================================", "blue", attrs=["bold"])
    cprint("         AI-SENTINEL", "blue", attrs=["bold"])
    cprint("===================================", "blue", attrs=["bold"])

    ip = input(colored("\n[AI-SENTINEL] IP cible > ","cyan",attrs=["bold"]))

    analyser_systeme("trafic_reseau.csv", ip)
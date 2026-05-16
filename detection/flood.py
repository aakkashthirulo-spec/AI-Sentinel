from collections import defaultdict

SEUIL_FLOOD = 100

def detecter_flood(donnees, ip):
    comptage = defaultdict(int)

    for log in donnees:
        comptage[log['ip_source']] += 1

    nb_requetes = comptage[ip]
    if nb_requetes > SEUIL_FLOOD:
        return (
            True,
            f"❌ FLOOD DÉTECTÉ "
            f"({nb_requetes} requêtes)"
        )

    return (
        False,
        "✅ Aucun flood détecté"
    )
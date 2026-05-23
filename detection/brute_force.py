SEUIL_BRUTE_FORCE = 5

def detecter_brute_force(donnees, ip):
    tentatives = 0
    for log in donnees:
        if (log['ip_source'] == ip and "ADMIN:" in log['payload_texte']):
            tentatives += 1
    if tentatives >= SEUIL_BRUTE_FORCE:
        return (True, f" BRUTE FORCE SSH ({tentatives} tentatives)")

    return (False," Aucun brute force détecté")
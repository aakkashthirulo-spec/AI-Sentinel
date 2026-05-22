SEUIL_BRUTE_FORCE = 5

def detecter_brute_force(donnees, ip):
    tentatives = 0
    for log in donnees:
        if (log['ip_source'] == ip and log['port'] == "22" and log['validation_flag'] == 0):
            tentatives += 1
    if tentatives >= SEUIL_BRUTE_FORCE:
        return (True,f" BRUTE FORCE SSH ", f"({tentatives} tentatives)")

    return (False," Aucun brute force détecté")
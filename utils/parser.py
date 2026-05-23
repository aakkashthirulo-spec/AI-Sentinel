import csv


def charger_logs(chemin_fichier):
    donnees = []
    try:
        with open(chemin_fichier,mode='r',encoding='utf-8') as fichier:
            lecteur = csv.DictReader(fichier)

            for ligne in lecteur:
                ligne['ip_source'] = ligne['ip_source'].strip()

                # Payload texte
                payload = str(ligne.get('payload_num', '')).upper()
                ligne['payload_texte'] = payload

                # Payload numérique
                try:
                    ligne['payload_num'] = float(ligne.get('payload_num', 0))
                except ValueError:
                    ligne['payload_num'] = 0.0

                # Heure
                try:
                    heure_complete = ligne.get('heure', '12:00:00')
                    try:
                        ligne['heure'] = int(heure_complete.split(":")[0])
                    except:
                        ligne['heure'] = 12
                except:
                    ligne['heure'] = 12

                # Validation
                try:
                    ligne['validation_flag'] = int(ligne.get('validation_flag', 1))
                except:
                    ligne['validation_flag'] = 1

                # Port
                ligne['port'] = str(ligne.get('port', ''))

                # Pays
                ligne['pays'] = str(ligne.get('pays', '')).upper()

                donnees.append(ligne)

    except FileNotFoundError:
        print(f"Fichier introuvable : {chemin_fichier}")
    return donnees
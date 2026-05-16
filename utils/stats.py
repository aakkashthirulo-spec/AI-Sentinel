import math

# Calcule l'écart à la norme (Z-score) pour chaque valeur.
def calculer_zscores(liste_tailles):
    n = len(liste_tailles)
    if n < 2:
        return [0] * n

    moyenne = sum(liste_tailles) / n
    somme_carres = sum((x - moyenne) ** 2 for x in liste_tailles)
    ecart_type = math.sqrt(somme_carres / n)

    if ecart_type == 0:
        return [0] * n
    
    return [(x - moyenne) / ecart_type for x in liste_tailles]
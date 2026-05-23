#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

// Définition de la structure d'un paquet réseau
typedef struct {
    char heure[15];
    char ip_source[16];
    int port;
    char pays[5];
    int payload_num;       // Taille des données transférées
    char payload_content[128]; // Contenu (utile pour détecter les injections)
} TrameReseau;

// Fonction pour obtenir l'heure actuelle au format HH:MM:SS
void obtenir_heure_actuelle(char *buffer) {
    time_t rawtime;
    struct tm *timeinfo;
    time(&rawtime);
    timeinfo = localtime(&rawtime);
    strftime(buffer, 15, "%H:%M:%S", timeinfo);
}

// Fonction modulaire pour écrire une trame dans le fichier de log
void ecrire_log(FILE *fichier, TrameReseau *trame) {
    if (fichier == NULL || trame == NULL) {
        return; // Protection contre les pointeurs nuls
    }
    
    // Format attendu par le script Python (CSV)
    fprintf(fichier, "%s,%s,%d,%s,%d,%s\n",
            trame->heure,
            trame->ip_source,
            trame->port,
            trame->pays,
            trame->payload_num,
            trame->payload_content);
            
    fflush(fichier); // Force l'écriture immédiate sur le disque pour le "Live Mode" Python
}

// Fonction pour simuler la capture d'un trafic suspect ou normal
void capturer_trafic(FILE *fichier, int nombre_de_paquets, const char *ip_cible) {
    TrameReseau trame_actuelle;
    
    // Simulation de différents types de trafic pour tester l'IA Python
    const char *pays_possibles[] = {"FR", "US", "RU", "CN", "BR"};
    const char *payloads_possibles[] = {
        "GET / HTTP/1.1", 
        "POST /login HTTP/1.1", 
        "' OR '1'='1", // Simulation d'injection SQL
        "admin:admin123", // Simulation de Brute Force
        "SYN_PACKET" // Simulation de Scan/Flood
    };

    printf("[C-SENTINEL] Début de la capture sur l'interface (Simulation)...\n");

    for (int i = 0; i < nombre_de_paquets; i++) {
        obtenir_heure_actuelle(trame_actuelle.heure);
        
        // Alterne entre l'IP cible et des IP aléatoires
        if (i % 3 == 0) {
            strcpy(trame_actuelle.ip_source, ip_cible);
        } else {
            sprintf(trame_actuelle.ip_source, "192.168.1.%d", (rand() % 254) + 1);
        }

        trame_actuelle.port = (rand() % 1000) + 20; // Ports aléatoires
        strcpy(trame_actuelle.pays, pays_possibles[rand() % 5]);
        trame_actuelle.payload_num = (rand() % 1500) + 40; // Taille aléatoire
        strcpy(trame_actuelle.payload_content, payloads_possibles[rand() % 5]);

        // Écriture via pointeur
        ecrire_log(fichier, &trame_actuelle);
        
        // Pause pour simuler le flux réseau temps réel (0.2 secondes)
        usleep(200000); 
    }
    
    printf("[C-SENTINEL] Capture terminée. Logs générés avec succès.\n");
}

int main() {
    // Initialisation du générateur aléatoire
    srand(time(NULL));
    
    const char *chemin_fichier = "trafic_reseau.csv";
    const char *ip_cible = "192.168.1.100"; // L'IP que tu passeras à ton Python
    
    // Ouverture du fichier en mode ajout (append) ou création
    FILE *fichier_log = fopen(chemin_fichier, "w");
    fprintf(fichier_log,"heure,ip_source,port,pays,payload_num,payload_content\n");
    if (fichier_log == NULL) {
        perror("Erreur lors de l'ouverture du fichier de log");
        return EXIT_FAILURE;
    }
    
    // Lancement de la capture (Génère 50 paquets pour le test)
    capturer_trafic(fichier_log, 50, ip_cible);
    
    fclose(fichier_log);
    
    return EXIT_SUCCESS;
}

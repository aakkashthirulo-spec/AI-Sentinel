import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# Variables globales pour garder une trace des processus en cours
processus_c = None
processus_python = None

def activer_protection():
    global processus_c, processus_python
    
    try:
        # 1. Lancement du programme C (en arrière-plan)
        # On suppose que le programme C compilé s'appelle 'sentinel' (ou 'sentinel.exe' sur Windows)
        if os.name == 'nt': # Si on est sur Windows
            processus_c = subprocess.Popen(["sentinel.exe"])
        else: # Si on est sur Linux/Mac
            processus_c = subprocess.Popen(["./sentinel"])
            
        # 2. Lancement de votre IA Python existante
        # Sur Windows, on peut lancer une nouvelle fenêtre console pour voir vos jolies couleurs
        if os.name == 'nt':
            processus_python = subprocess.Popen(["start", "cmd", "/c", "python analyse.py"], shell=True)
        else:
            # AJOUT ICI : Commande osascript insérée à sa place exacte pour Mac
            processus_python = subprocess.Popen(["osascript", "-e", f'tell app "Terminal" to do script "cd {os.getcwd()} && python3 sentinel.py 192.168.1.100"'])
            
        # Mise à jour visuelle de l'interface
        label_statut.config(text="STATUT : ACTIVÉ ET EN LIGNE", fg="green")
        btn_activer.config(state="disabled")
        btn_desactiver.config(state="normal")
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lancer les modules : {e}")

def desactiver_protection():
    global processus_c
    
    # On arrête le processus C qui tourne en arrière-plan
    if processus_c:
        processus_c.terminate()
        
    # Mise à jour de l'interface
    label_statut.config(text="STATUT : DÉSACTIVÉ", fg="red")
    btn_activer.config(state="normal")
    btn_desactiver.config(state="disabled")

# ==========================================
# CRÉATION DE LA FENÊTRE PRINCIPALE
# ==========================================
fenetre = tk.Tk()
fenetre.title("AI-SENTINEL - Panneau de Contrôle")
fenetre.geometry("400x250")
fenetre.configure(bg="#1e1e1e") # Fond sombre, style cybersécurité

# Titre
titre = tk.Label(fenetre, text="AI-SENTINEL", font=("Helvetica", 20, "bold"), bg="#1e1e1e", fg="#00ffff")
titre.pack(pady=20)

# Indicateur de statut
label_statut = tk.Label(fenetre, text="STATUT : DÉSACTIVÉ", font=("Helvetica", 12, "bold"), bg="#1e1e1e", fg="red")
label_statut.pack(pady=10)

# Bouton Activer
btn_activer = tk.Button(fenetre, text="Activer la Protection", font=("Helvetica", 12, "bold"), 
                        bg="#28a745", fg="white", command=activer_protection, width=20)
btn_activer.pack(pady=5)

# Bouton Désactiver
btn_desactiver = tk.Button(fenetre, text="Désactiver", font=("Helvetica", 12, "bold"), 
                           bg="#dc3545", fg="white", command=desactiver_protection, width=20, state="disabled")
btn_desactiver.pack(pady=5)

# Lancement de la boucle de l'interface
fenetre.mainloop()

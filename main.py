# main.py

import os
from file_processor import process_files_in_directory
from metadata import load_keywords_from_file
from utils import log_info

def main():
    """
    Point d'entrée principal du programme de renommage automatique de fichiers géographiques.
    """
    print("Bienvenue dans le programme de renommage automatique de fichiers géographiques.")
    # Demander le chemin du dossier à traiter
    folder_path = input("Veuillez entrer le chemin du dossier à traiter: ")

    # Vérification si le dossier existe
    if not os.path.isdir(folder_path):
        print("Le chemin fourni n'est pas un dossier valide ou n'existe pas.")
        return
    
    log_info(f"Traitement du dossier: {folder_path}")
    
    # Lancement du processus de renommage des fichiers
    process_files_in_directory(folder_path)
    
    print("Renommage terminé. Consultez le fichier log pour plus de détails.")

if __name__ == "__main__":
    main()

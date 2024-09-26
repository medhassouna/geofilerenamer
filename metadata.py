import json
import os

# Dictionnaire des mots-clés par défaut
keywords = {
    'adm': ['administratif', 'lieux_nommes', 'admin'],
    'cad': ['cadastre'],
    'zone': ['reglementee', 'zonage']
}

def load_keywords_from_file(file_path="metadata.json"):
    """
    Charge les mots-clés depuis un fichier JSON.
    """
    global keywords
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            keywords = json.load(f)
        print(f"Mots-clés chargés depuis {file_path}")
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé. Chargement des mots-clés par défaut.")
    except json.JSONDecodeError:
        print(f"Erreur de décodage JSON dans {file_path}. Chargement des mots-clés par défaut.")
    except Exception as e:
        print(f"Une erreur s'est produite lors du chargement de {file_path}: {e}")

def save_keywords_to_file(file_path="metadata.json"):
    """
    Sauvegarde les mots-clés dans un fichier JSON.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(keywords, f, ensure_ascii=False, indent=4)
        print(f"Les mots-clés ont été sauvegardés dans {file_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des mots-clés : {e}")

def add_keyword_to_prefix(base_name, prefix):
    """
    Propose d'ajouter un mot-clé pour un préfixe donné et sauvegarde la mise à jour.
    """
    choice = input(f"Le mot '{base_name}' n'a pas été trouvé pour le préfixe '{prefix}'. Voulez-vous l'ajouter à la liste des mots-clés ? (o/n) [o] : ").lower()

    if choice in ['o', '']:
        base_name_lower = base_name.lower()

        # Ajouter le mot dans la liste des mots-clés du préfixe s'il n'existe pas déjà
        if prefix in keywords:
            if base_name_lower not in keywords[prefix]:
                keywords[prefix].append(base_name_lower)
        else:
            keywords[prefix] = [base_name_lower]

        # Sauvegarder immédiatement après l'ajout
        save_keywords_to_file()
    else:
        print(f"Le mot '{base_name}' n'a pas été ajouté.")

# Charger les mots-clés depuis metadata.json au démarrage
load_keywords_from_file("metadata.json")

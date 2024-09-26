import os
from metadata import keywords, save_keywords_to_file, add_keyword_to_prefix
from utils import compare_words_insensitive

# Variables globales pour stocker les dernières entrées utilisateur (source, année, échelle)
last_source = None
last_year = None
last_scale = None

def detect_prefix(folder, base_name):
    """
    Détecte automatiquement le préfixe en fonction des mots-clés dans le nom du dossier ou du fichier.
    Parcourt le dictionnaire des keywords et compare les mots du nom du dossier et du fichier avec les mots-clés.
    """
    parent_folder = os.path.basename(os.path.normpath(folder))  # Récupère le nom du dossier parent

    for prefix, keyword_list in keywords.items():
        for keyword in keyword_list:
            if compare_words_insensitive(parent_folder, keyword) or compare_words_insensitive(base_name, keyword):
                return prefix
    return None

def get_metadata_for_file(base_name, files):
    """
    Récupère les métadonnées pour un fichier et demande à l'utilisateur s'il souhaite renommer.
    Si nécessaire, propose les dernières entrées utilisateur comme valeurs par défaut.
    """
    global last_source, last_year, last_scale
    folder = os.path.dirname(files[0])  # Récupère le dossier du fichier
    
    # Trouver si un fichier .shp existe dans le groupe
    shp_file = next((f for f in files if f.endswith('.shp')), None)

    # Si un fichier .shp existe, utiliser son nom de base (sans extension) pour la question
    if shp_file:
        base_name_to_display = os.path.splitext(os.path.basename(shp_file))[0]
    else:
        # Si ce n'est pas un shapefile, utiliser le nom complet du fichier
        base_name_to_display = os.path.basename(files[0])

    # Demander si l'utilisateur veut renommer le fichier, avec 'o' comme réponse par défaut
    rename_choice = input(f"Souhaitez-vous renommer le fichier {base_name_to_display}? (o/n) [o] : ").lower()
    
    if rename_choice not in ['o', '']:
        print(f"Le fichier '{base_name_to_display}' ne sera pas renommé.")
        return None

    # Détecter le préfixe ou demander à l'utilisateur
    prefix = detect_prefix(folder, base_name) or ask_for_prefix(base_name, files[0])

    # Demander la source avec la possibilité d'ignorer
    source = input(f"Veuillez entrer la source (ex: bdtopo) ou appuyez sur Entrée pour réutiliser '{last_source}' ou tapez 'n' pour ignorer : ").strip()
    if source.lower() == 'n':  # Si l'utilisateur tape 'n', on garde la source vide ou inconnue
        source = "inconnue"
    elif not source:
        source = last_source  # Réutilise la dernière source uniquement si l'utilisateur appuie sur Entrée
    last_source = source  # Mémoriser la dernière source entrée

    # Demander l'année avec la possibilité d'ignorer
    year = input(f"Veuillez entrer l'année des données (format: YYYY) ou appuyez sur Entrée pour réutiliser '{last_year}' ou tapez 'n' pour ignorer : ").strip()
    if year.lower() == 'n':  # Si l'utilisateur tape 'n', on garde l'année vide ou inconnue
        year = "inconnue"
    elif not year:
        year = last_year  # Réutilise la dernière année si l'utilisateur appuie sur Entrée
    last_year = year

    # Demander l'échelle avec la possibilité d'ignorer
    scale = input(f"Veuillez entrer l'échelle des données (ex: 10K, 25K) ou appuyez sur Entrée pour réutiliser '{last_scale}' ou tapez 'n' pour ignorer : ").strip()
    if scale.lower() == 'n':  # Si l'utilisateur tape 'n', on garde l'échelle vide ou inconnue
        scale = "inconnue"
    elif not scale:
        scale = last_scale  # Réutilise la dernière échelle si l'utilisateur appuie sur Entrée
    last_scale = scale

    return {
        'prefix': prefix,
        'source': source,
        'year': year,
        'scale': scale
    }

def validate_or_change_prefix(detected_prefix, base_name):
    """
    Permet à l'utilisateur de valider ou de changer le préfixe détecté pour un fichier.
    'o' est considéré comme la réponse par défaut.
    """
    print(f"Le préfixe détecté pour {base_name} est : {detected_prefix}.")
    choice = input("Voulez-vous valider ce préfixe ? (o/n) [o] : ").lower()
    
    if choice in ['', 'o']:  # Interprète une réponse vide comme 'o'
        return detected_prefix
    else:
        return ask_for_prefix(base_name)

def ask_for_prefix(base_name, full_file_path):
    """
    Demande à l'utilisateur de saisir un préfixe s'il n'a pas été détecté automatiquement.
    Affiche le chemin du dossier parent du fichier (sans inclure le nom du fichier).
    """
    # # Debugging: Affiche les préfixes avant de les afficher à l'utilisateur
    # print("DEBUG: Préfixes disponibles avant affichage :")
    # print(keywords)

    # Les préfixes du dictionnaire keywords
    print(f"Préfixes disponibles : {list(keywords.keys())}")
    
    folder_path = os.path.dirname(full_file_path)
    print(f"Chemin complet du dossier : {folder_path}")

    # Demande à l'utilisateur d'entrer un préfixe
    prefix_input = input(f"Aucun préfixe détecté pour {base_name}. Veuillez entrer un préfixe parmi ceux listés : ")

    # Vérifie que le préfixe existe dans le dictionnaire
    while prefix_input not in keywords:
        print("Préfixe invalide. Veuillez choisir un préfixe parmi ceux listés.")
        prefix_input = input(f"Veuillez entrer un préfixe valide pour {base_name} : ")

    # Propose d'ajouter le mot-clé s'il n'est pas déjà dans le dictionnaire
    if base_name.lower() not in keywords[prefix_input]:
        add_keyword_to_prefix(base_name, prefix_input)

    return prefix_input

def validate_year(year):
    """
    Valide que l'année est au format YYYY.
    """
    return bool(re.match(r'^\d{4}$', year))

def validate_scale(scale):
    """
    Valide que l'échelle est au format valide (ex: 10K, 200K, 1K, 2000K).
    """
    return bool(re.match(r'^\d{1,4}K$', scale, re.IGNORECASE))

def get_valid_year():
    """
    Demande à l'utilisateur de fournir une année au format YYYY.
    Si aucune entrée n'est faite, l'utilisateur doit entrer une année valide.
    """
    while True:
        year = input("Veuillez entrer l'année des données (format: YYYY) : ").strip()
        if not year:  # Si l'utilisateur appuie sur Entrée, pas de valeur par défaut
            return None
        if validate_year(year):
            return year
        print("Format d'année invalide. Veuillez entrer une année au format YYYY (ex: 2023).")

def get_valid_scale():
    """
    Demande à l'utilisateur de fournir une échelle au format valide (ex: 10K, 200K).
    Si aucune entrée n'est faite, l'utilisateur doit entrer une échelle valide.
    """
    while True:
        scale = input("Veuillez entrer l'échelle des données (ex: 10K, 25K) : ").strip()
        if not scale:  # Si l'utilisateur appuie sur Entrée, pas de valeur par défaut
            return None
        if validate_scale(scale):
            return scale.upper()  # Normaliser la sortie pour être en majuscules
        print("Format d'échelle invalide. Veuillez entrer une échelle au format valide (ex: 10K, 200K, 1K).")
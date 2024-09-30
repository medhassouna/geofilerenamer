import os
from metadata import keywords, save_keywords_to_file, add_keyword_to_prefix
from utils import compare_words_insensitive

# Variables globales pour stocker les dernières entrées utilisateur (source, année, échelle)
# Ces variables permettent de réutiliser les dernières valeurs saisies par l'utilisateur
last_source = None
last_year = None
last_scale = None

def detect_prefix(folder, base_name):
    """
    Détecte automatiquement le préfixe basé sur le nom du dossier ou du fichier.
    Parcourt le dictionnaire `keywords` pour identifier un préfixe associé aux mots-clés
    trouvés dans le nom du dossier parent ou du fichier.
    
    Args:
        folder (str): Le chemin du dossier contenant le fichier.
        base_name (str): Le nom de base du fichier (sans extension).
        
    Returns:
        str: Le préfixe détecté ou None s'il n'est pas trouvé.
    """
    # Extraire le nom du dossier parent
    parent_folder = os.path.basename(os.path.normpath(folder))

    # Parcourir chaque préfixe et sa liste de mots-clés pour faire une correspondance
    for prefix, keyword_list in keywords.items():
        for keyword in keyword_list:
            # Comparer de manière insensible à la casse avec le dossier parent ou le nom du fichier
            if compare_words_insensitive(parent_folder, keyword) or compare_words_insensitive(base_name, keyword):
                return prefix
    return None

def get_metadata_for_file(base_name, files):
    """
    Collecte les métadonnées nécessaires (préfixe, source, année, échelle) pour un fichier.
    Demande à l'utilisateur de valider ou de modifier certaines informations si elles sont déjà fournies.
    
    Args:
        base_name (str): Nom de base du fichier (sans extension).
        files (list): Liste des fichiers associés (shapefiles ou autres formats).

    Returns:
        dict: Un dictionnaire contenant les métadonnées (`prefix`, `source`, `year`, `scale`).
    """
    global last_source, last_year, last_scale  # Réutilisation des dernières valeurs
    folder = os.path.dirname(files[0])  # Récupérer le dossier du premier fichier

    # Utiliser .shp si c'est un groupe de shapefiles, sinon utiliser le premier fichier
    shp_file = next((f for f in files if f.endswith('.shp')), files[0])
    base_name_to_display = os.path.basename(shp_file)  # Afficher le nom avec extension .shp ou autre

    # Demander si l'utilisateur veut renommer le fichier
    rename_choice = input(f"Souhaitez-vous renommer le fichier {base_name_to_display}? (o/n) [o] : ").lower()

    # Si l'utilisateur ne souhaite pas renommer, retourner None
    if rename_choice not in ['o', '']:
        print(f"Le fichier '{base_name_to_display}' ne sera pas renommé.")
        return None

    # Détecter le préfixe automatiquement
    detected_prefix = detect_prefix(folder, base_name)
    
    # Proposer à l'utilisateur de valider ou modifier le préfixe détecté
    prefix = validate_or_change_prefix(detected_prefix, base_name)

    # Collecter les autres métadonnées : source, année, échelle avec possibilité de réutiliser ou d'ignorer
    source = get_user_input_with_default("source", last_source)
    last_source = source  # Mémoriser la dernière valeur saisie

    year = get_user_input_with_default("année des données (format: YYYY)", last_year)
    last_year = year  # Mémoriser la dernière année saisie

    scale = get_user_input_with_default("échelle des données (ex: 10K, 25K)", last_scale)
    last_scale = scale  # Mémoriser la dernière échelle saisie

    # Retourner les métadonnées collectées
    return {
        'prefix': prefix,
        'source': source,
        'year': year,
        'scale': scale
    }
    
def get_user_input_with_default(label, default_value):
    """
    Demande à l'utilisateur une entrée avec une valeur par défaut. Si l'utilisateur ne fournit pas
    de nouvelle valeur, la valeur par défaut est utilisée. L'utilisateur peut également taper 'n'
    pour ignorer cette donnée.

    Args:
        label (str): Le texte à afficher pour demander l'entrée de l'utilisateur.
        default_value (str): La valeur par défaut à réutiliser si l'utilisateur ne fournit pas d'entrée.
        
    Returns:
        str: La valeur saisie par l'utilisateur ou la valeur par défaut.
    """
    # Formuler la question avec la valeur par défaut et la possibilité d'ignorer ('n')
    user_input = input(f"Veuillez entrer {label} ou appuyez sur Entrée pour réutiliser '{default_value}' ou tapez ( i ) pour ignorer : ").strip()
    
    if user_input.lower() == 'i':
        return "inconnue"  # Si 'n' est saisi, renvoyer 'inconnue'
    
    # Si aucune saisie n'est faite, réutiliser la valeur par défaut
    return user_input if user_input else default_value

def validate_or_change_prefix(detected_prefix, base_name):
    """
    Permet à l'utilisateur de valider ou de modifier le préfixe détecté.
    Si l'utilisateur souhaite modifier le préfixe, il peut en entrer un nouveau.
    
    Args:
        detected_prefix (str): Le préfixe détecté automatiquement.
        base_name (str): Le nom de base du fichier.
    
    Returns:
        str: Le préfixe validé ou modifié.
    """
    # Afficher le préfixe détecté et demander à l'utilisateur de le valider ou de le modifier
    print(f"Le préfixe détecté pour le fichier '{base_name}' est : '{detected_prefix}'.")
    choice = input(f"Voulez-vous valider ce préfixe ? (o/n) [o] : ").lower()

    # Si l'utilisateur valide (par défaut 'o'), retourner le préfixe détecté
    if choice in ['o', '']:
        return detected_prefix
    
    # Sinon, demander un nouveau préfixe à l'utilisateur
    return ask_for_prefix(base_name, base_name)

def ask_for_prefix(base_name, full_file_path):
    """
    Demande à l'utilisateur de saisir un préfixe valide si celui détecté ne convient pas.

    Args:
        base_name (str): Nom de base du fichier.
        full_file_path (str): Chemin complet du fichier pour affichage contextuel.
    
    Returns:
        str: Le préfixe validé ou saisi par l'utilisateur.
    """
    print(f"Préfixes disponibles : {list(keywords.keys())}")
    
    # Afficher le chemin complet du dossier parent
    folder_path = os.path.dirname(full_file_path)
    print(f"Chemin complet du dossier : {folder_path}")

    # Demander à l'utilisateur d'entrer un préfixe valide
    prefix_input = input(f"Veuillez entrer un préfixe pour '{base_name}' parmi ceux listés : ")

    # Boucle jusqu'à ce qu'un préfixe valide soit saisi
    while prefix_input not in keywords:
        print("Préfixe invalide. Veuillez choisir un préfixe parmi ceux listés.")
        prefix_input = input(f"Veuillez entrer un préfixe valide pour '{base_name}' : ")

    # Proposer d'ajouter le mot-clé au dictionnaire s'il n'est pas déjà présent
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
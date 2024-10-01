import unicodedata
import os
import re
import json
from datetime import datetime

# Liste des mots de liaison à supprimer des noms
JOIN_WORDS = ['de', 'du', 'des', 'd', 'la', 'le', 'les', 'et', 'au', 'aux', 'sur', 'à', 'ou']

def remove_accents_and_special_chars(name):
    """
    Nettoie une chaîne en supprimant les accents et les caractères spéciaux, 
    puis en remplaçant tout caractère non alphanumérique par un underscore (_).
    
    Parameters:
        name (str): Le nom de fichier à nettoyer.
        
    Returns:
        str: La chaîne nettoyée sans accents ni caractères spéciaux.
    """
    nfkd_form = unicodedata.normalize('NFKD', name)
    without_accents = ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    return re.sub(r'[^a-zA-Z0-9]', '_', without_accents)  # Remplacer les caractères non alphanumériques par _

def split_into_segments(name):
    """
    Sépare le nom d'un fichier en segments basés sur les majuscules, les chiffres, les tirets et les underscores.
    
    Parameters:
        name (str): Le nom de fichier à segmenter.
        
    Returns:
        list: Une liste de segments découpés du nom.
    """
    normalized_name = remove_accents_and_special_chars(name)
    return re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z])|[A-Z]+|[0-9]+|[-_]', normalized_name)

def process_segments(segments):
    """
    Applique le format camelCase à une liste de segments en ignorant les mots de liaison, tirets et underscores.
    
    Parameters:
        segments (list): La liste des segments à traiter.
        
    Returns:
        str: Le nom formaté en camelCase.
    """
    filtered_segments = [
        segment for segment in segments if segment not in ['-', '_'] and segment.lower() not in JOIN_WORDS
    ]
    if not filtered_segments:
        return ""
    first_word = filtered_segments[0].lower()
    camel_case_segments = [first_word] + [word.capitalize() for word in filtered_segments[1:]]
    return ''.join(camel_case_segments)

def load_prefixes_from_json(file_path='metadata.json'):
    """
    Charge les préfixes depuis le fichier metadata.json.
    
    Args:
        file_path (str): Le chemin vers le fichier JSON contenant les préfixes.
        
    Returns:
        list: Une liste des préfixes disponibles.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return list(data.keys())  # Retourne uniquement les clés (les préfixes)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} n'a pas été trouvé.")
        return []
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON dans {file_path} : {e}")
        return []

def is_file_already_renamed(filename, prefixes):
    """
    Vérifie si un fichier a déjà été renommé selon la convention :
    [prefix]_[suffix]_[nomCamelCase]_[source]_[année]_[échelle] (source, année, et échelle sont optionnelles).
    
    Args:
        filename (str): Le nom du fichier à vérifier, sans extension.
        prefixes (list): Liste des préfixes dynamiques à vérifier.
        
    Returns:
        bool: True si le fichier est déjà renommé, sinon False.
    """
    # Retirer l'extension pour ne vérifier que le nom de base
    base_name = os.path.splitext(filename)[0]

    # Construire une regex dynamique en fonction des préfixes chargés depuis le fichier JSON
    prefix_pattern = f"^({'|'.join(prefixes)})"

    # Pattern de correspondance stricte avec CamelCase et parties optionnelles
    pattern_with_suffix = rf"{prefix_pattern}(_[a-z]+)?_[a-zA-Z][a-zA-Z0-9]*(_[a-zA-Z0-9]+)?(_\d{{4}})?(_\d+[KM])?"

    # Vérifier si le nom de base correspond au pattern
    result = bool(re.match(pattern_with_suffix, base_name))
    
    return result

def log_info(message):
    """
    Enregistre les messages d'information dans un fichier log avec un timestamp.
    Gère les exceptions liées à l'écriture dans le fichier.
    """
    try:
        with open("process.log", "a") as log_file:
            log_file.write(f"{datetime.now()}: {message}\n")
    except IOError as e:
        print(f"Erreur lors de l'écriture dans le fichier log: {e}")

def compare_words_insensitive(name, keyword):
    """
    Compare deux chaînes insensiblement à la casse, mot par mot, en ignorant les mots de liaison.
    Utilise les mots exclus de la liste JOIN_WORDS.
    
    Args:
        name (str): Nom à comparer.
        keyword (str): Mot-clé à comparer avec le nom.
        
    Returns:
        bool: True si tous les mots du mot-clé sont présents dans le nom, sinon False.
    """
    name_parts = [word.lower() for word in name.split() if word.lower() not in JOIN_WORDS]
    keyword_parts = [word.lower() for word in keyword.split()]
    
    return all(part in name_parts for part in keyword_parts)

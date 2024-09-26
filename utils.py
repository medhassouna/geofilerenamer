# utils.py

import unicodedata
import re
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
    # Normalisation Unicode pour retirer les accents
    nfkd_form = unicodedata.normalize('NFKD', name)
    without_accents = ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    # Remplacer les caractères non alphanumériques par des underscores
    return re.sub(r'[^a-zA-Z0-9]', '_', without_accents)

def split_into_segments(name):
    """
    Sépare le nom d'un fichier en segments basés sur les majuscules, les chiffres, les tirets et les underscores.
    Parameters:
        name (str): Le nom de fichier à segmenter.
    Returns:
        list: Une liste de segments découpés du nom.
    """
    # Supprimer les accents et normaliser les caractères spéciaux
    normalized_name = remove_accents_and_special_chars(name)
    # Expression régulière pour découper le nom en segments
    segments = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z])|[A-Z]+|[0-9]+|[-_]', normalized_name)
    return segments

def process_segments(segments):
    """
    Applique le format camelCase à une liste de segments en ignorant les mots de liaison, tirets et underscores.
    Parameters:
        segments (list): La liste des segments à traiter.
    Returns:
        str: Le nom formaté en camelCase.
    """
    # Filtrer les segments en ignorant les tirets, underscores et mots de liaison
    filtered_segments = [
        segment for segment in segments if segment not in ['-', '_'] and segment.lower() not in JOIN_WORDS
    ]
    # Si aucun segment pertinent n'est trouvé, retourner une chaîne vide
    if not filtered_segments:
        return ""
    # Le premier segment est en minuscule, les suivants avec majuscule initiale (camelCase)
    first_word = filtered_segments[0].lower()
    camel_case_segments = [first_word] + [word.capitalize() for word in filtered_segments[1:]]
    # Retourner le nom final en camelCase
    return ''.join(camel_case_segments)

def is_file_already_renamed(filename):
    """
    Vérifie si un fichier a déjà été renommé selon la convention :
    [prefixe]_[nomFichierCamelCase]_[source]_[année].
    Le fichier est considéré comme déjà renommé si un pattern correspondant est détecté.
    """
    pattern_with_suffix = r"^[a-z]+(_[a-z]+)?_[a-zA-Z0-9]+_[a-zA-Z0-9]+_\d{4}.*"
    return bool(re.match(pattern_with_suffix, filename))

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
    """
    name_parts = [word.lower() for word in name.split() if word.lower() not in JOIN_WORDS]
    keyword_parts = [word.lower() for word in keyword.split()]
    
    return all(part in name_parts for part in keyword_parts)

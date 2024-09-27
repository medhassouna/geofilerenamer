import os
from metadata_handler import get_metadata_for_file
from naming_convention import apply_naming_convention, identify_suffix
from utils import log_info, is_file_already_renamed

# Liste des extensions prises en charge, y compris shapefiles et autres formats géospatiaux courants
SUPPORTED_EXTENSIONS = ['.shp', '.shx', '.dbf', '.prj', '.sld', '.cpg', '.xml', '.shp.xml', '.qml', '.qlr', '.gpkg', 
                        '.json', '.geojson', '.csv', '.kmz', '.KMZ', '.kml', '.KML', '.dwg', '.DWG']
# Extensions spécifiques aux fichiers composant un groupe de shapefiles
SHAPEFILE_EXTENSIONS = ['.shp', '.shx', '.dbf', '.prj', '.sld', '.cpg', '.xml', '.shp.xml', '.qml', '.qlr']


def collect_files_by_extension(folder, extensions):
    """
    Parcourt un dossier et regroupe les fichiers selon leur extension.
    Cela permet de traiter les fichiers qui partagent le même nom de base mais avec des extensions différentes
    (ex. shapefiles ou autres formats géospatiaux).
    
    Args:
        folder (str): Le chemin vers le dossier à parcourir.
        extensions (list): Liste des extensions de fichiers à rechercher.
        
    Returns:
        dict: Dictionnaire avec le nom de base comme clé et une liste des fichiers correspondants comme valeur.
    """
    file_groups = {}
    
    # Parcourt récursivement le dossier à la recherche de fichiers avec les extensions prises en charge
    for root, dirs, files in os.walk(folder):
        valid_files = [file for file in files if any(file.endswith(ext) for ext in extensions)]
        
        # Ignorer les dossiers sans fichiers valides
        if not valid_files:
            continue

        for file in valid_files:
            base_name, ext = os.path.splitext(file)
            
            # Grouper les fichiers par nom de base (sans l'extension)
            if base_name not in file_groups:
                file_groups[base_name] = []
            file_groups[base_name].append(os.path.join(root, file))  # Ajouter le chemin complet du fichier
    
    return file_groups


def process_files_in_directory(folder):
    """
    Traite les fichiers dans le dossier spécifié en regroupant les fichiers de même base
    et en les renommant selon les conventions définies.
    
    Args:
        folder (str): Le chemin vers le dossier contenant les fichiers à traiter.
    """
    # Collecte des fichiers par extension dans le dossier donné
    file_groups = collect_files_by_extension(folder, SUPPORTED_EXTENSIONS)

    # Si aucun fichier valide n'est trouvé, arrêter le processus
    if not file_groups:
        print(f"Aucun fichier valide trouvé dans le dossier {folder}.")
        return

    # Traiter chaque groupe de fichiers (fichiers ayant le même nom de base)
    for base_name, files in file_groups.items():
        process_file_group(base_name, files)


def process_file_group(base_name, files):
    """
    Traite un groupe de fichiers ayant le même nom de base. Collecte les métadonnées,
    détecte le suffixe si nécessaire et renomme chaque fichier dans le groupe.

    Args:
        base_name (str): Nom de base du groupe de fichiers.
        files (list): Liste des fichiers associés au nom de base.
    """
    file_dir = os.path.dirname(files[0])  # Récupère le dossier où se trouvent les fichiers
    print(f"Renommage des fichiers dans le dossier : {file_dir}")

    # Afficher le fichier .shp pour les groupes shapefiles, sinon un fichier général
    shp_file = next((f for f in files if f.endswith('.shp')), files[0])
    base_name_with_extension = os.path.basename(shp_file) if shp_file.endswith('.shp') else os.path.basename(files[0])

    # Vérifier si le fichier a déjà été renommé selon la convention
    if is_file_already_renamed(base_name):
        print(f"Le fichier '{base_name}' est déjà renommé selon la convention.")
        return

    # Proposer de modifier le nom de base
    base_name_modified = ask_if_change_base_name(base_name_with_extension, base_name, files, file_dir)

    # Obtenir les métadonnées (préfixe, source, année, échelle)
    metadata = get_metadata_for_file(base_name_modified, files)

    if metadata is None:
        return  # Si aucune métadonnée n'est fournie, passer au groupe suivant

    # Détecter le suffixe uniquement pour les groupes shapefiles
    if any(f.endswith('.shp') for f in files):
        suffix = identify_suffix(shp_file) if shp_file else 'unknown'
    else:
        suffix = ''  # Pas de suffixe pour les autres types de fichiers

    # Renommer tous les fichiers du groupe avec les métadonnées et le suffixe
    rename_file_group(files, metadata['prefix'], metadata['source'], metadata['year'], metadata['scale'], suffix)


def ask_if_change_base_name(base_name_with_extension, base_name, files, file_dir):
    """
    Demande à l'utilisateur s'il souhaite modifier le nom de base d'un fichier.
    Si l'utilisateur accepte, il est invité à saisir un nouveau nom de base qui sera appliqué à tous les fichiers du groupe.

    Args:
        base_name_with_extension (str): Nom de base avec l'extension à afficher à l'utilisateur.
        base_name (str): Nom de base d'origine.
        files (list): Liste des fichiers appartenant au groupe.
        file_dir (str): Dossier où se trouvent les fichiers.

    Returns:
        str: Le nom de base modifié ou d'origine.
    """
    # Demander si l'utilisateur souhaite modifier le nom de base
    change_base_name = input(f"Souhaitez-vous modifier le nom de base '{base_name_with_extension}' ? (o/n) [n] : ").lower()

    if change_base_name in ['o', 'oui']:
        # Demander à l'utilisateur de saisir un nouveau nom de base
        base_name_modified_input = input(f"Entrez le nouveau nom de base pour '{base_name_with_extension}' : ").strip()
        if base_name_modified_input:
            print(f"Le nom de base '{base_name}' a été modifié en '{base_name_modified_input}'.")
            base_name = base_name_modified_input

            # Renommer temporairement tous les fichiers du groupe avec le nouveau nom de base
            for i, file in enumerate(files):
                extension = os.path.splitext(file)[1]
                new_file_path = os.path.join(file_dir, f"{base_name}{extension}")
                os.rename(file, new_file_path)  # Appliquer le renommage
                files[i] = new_file_path  # Mettre à jour la liste des fichiers

    return base_name  # Retourner le nom de base modifié ou d'origine


def rename_file_group(files, prefix, source, year, scale, suffix):
    """
    Renomme un groupe de fichiers en fonction des métadonnées fournies et du suffixe détecté.
    
    Args:
        files (list): Liste des fichiers à renommer.
        prefix (str): Préfixe à ajouter au nom de fichier.
        source (str): Source des données à ajouter au nom de fichier.
        year (str): Année des données à ajouter au nom de fichier.
        scale (str): Échelle des données à ajouter au nom de fichier.
        suffix (str): Suffixe basé sur le type de géométrie (pour les shapefiles).
    """
    for file in files:
        if not is_file_already_renamed(file):
            # Appliquer la convention de nommage en utilisant les métadonnées
            new_name = apply_naming_convention(file, prefix, suffix, source, year, scale)

            # Vérifier que le nouveau nom est valide
            if isinstance(new_name, str):
                log_info(f"Renommage de {file} en {new_name}")
                print(f"Renommage de '{file}' en '{new_name}'")
                os.rename(file, os.path.join(os.path.dirname(file), new_name))  # Appliquer le renommage
            else:
                print(f"Erreur : Le nouveau nom pour le fichier '{file}' n'est pas valide : {new_name}")
        else:
            print(f"Le fichier '{file}' est déjà renommé selon la convention.")

import os
from metadata_handler import get_metadata_for_file
from naming_convention import apply_naming_convention, identify_suffix
from utils import log_info, is_file_already_renamed, load_prefixes_from_json

# Liste des extensions prises en charge, y compris shapefiles et autres formats géospatiaux courants
SUPPORTED_EXTENSIONS = ['.shp', '.shx', '.dbf', '.prj', '.sld', '.cpg', '.shp.xml', '.xml', '.qml', '.qlr', '.gpkg', 
                        '.json', '.geojson', '.csv', '.kmz', '.KMZ', '.kml', '.KML', '.dwg', '.DWG', '.qpj', '.cst', '.sbn', '.sbx']

# Extensions spécifiques aux fichiers composant un groupe de shapefiles
SHAPEFILE_EXTENSIONS = ['.shp', '.shx', '.dbf', '.prj', '.sbn', '.sbx', '.sld', '.cpg', '.shp.xml', '.xml', '.qml', '.qlr', '.qpj', '.cst']

# Charger les préfixes dynamiques une fois depuis le fichier metadata.json
dynamic_prefixes = load_prefixes_from_json()

def collect_files_by_extension(folder, extensions):
    """
    Parcourt un dossier et regroupe les fichiers selon leur extension.
    Cela permet de traiter les fichiers qui partagent le même nom de base mais avec des extensions différentes.
    Les fichiers .xml qui appartiennent à un groupe shapefile doivent être regroupés avec le reste du groupe.
    """
    file_groups = {}

    for root, dirs, files in os.walk(folder):
        valid_files = [file for file in files if any(file.endswith(ext) for ext in extensions)]
        if not valid_files:
            continue

        for file in valid_files:
            if file.endswith('.shp.xml'):
                base_name = file[:-8]  # Retire ".shp.xml" du nom du fichier
            else:
                base_name, ext = os.path.splitext(file)

            # Associer les fichiers .xml qui appartiennent au groupe shapefile
            if ext == '.xml' and base_name in file_groups:
                # Vérifier si ce fichier .xml appartient à un groupe shapefile
                if any(f.endswith('.shp') for f in file_groups[base_name]):
                    file_groups[base_name].append(os.path.join(root, file))
                    continue

            if base_name not in file_groups:
                file_groups[base_name] = []
            file_groups[base_name].append(os.path.join(root, file))  # Ajouter le chemin complet du fichier
    
    return file_groups

def process_files_in_directory(folder):
    """
    Traite les fichiers dans le dossier spécifié en regroupant les fichiers de même base
    et en les renommant selon les conventions définies.
    """
    file_groups = collect_files_by_extension(folder, SUPPORTED_EXTENSIONS)

    if not file_groups:
        print(f"Aucun fichier valide trouvé dans le dossier {folder}.")
        return

    for base_name, files in file_groups.items():
        process_file_group(base_name, files)

def process_file_group(base_name, files):
    """
    Traite un groupe de fichiers ayant le même nom de base. Collecte les métadonnées,
    détecte le suffixe si nécessaire et renomme chaque fichier dans le groupe.
    """
    file_dir = os.path.dirname(files[0])
    print(f"Renommage des fichiers dans le dossier : {file_dir}")

    # Identifier le fichier .shp comme représentant principal du groupe shapefile
    shp_file = next((f for f in files if f.endswith('.shp')), None)
    base_name_with_extension = os.path.basename(shp_file) if shp_file else os.path.basename(files[0])

    # Vérifier si le fichier est déjà renommé (avec les préfixes dynamiques)
    if is_file_already_renamed(base_name, dynamic_prefixes):
        print(f"Le fichier '{base_name}' est déjà renommé selon la convention.")
        return

    # Proposer de modifier le nom de base
    base_name_modified = ask_if_change_base_name(base_name_with_extension, base_name, files, file_dir)

    # Renommer temporairement les fichiers avec le nouveau nom de base
    rename_files_with_new_base_name(base_name, base_name_modified, files, file_dir)

    # Mise à jour du nom de base modifié après renommage temporaire
    base_name_modified = os.path.splitext(os.path.basename(files[0]))[0]

    # Si un fichier .shp est trouvé, détecter le suffixe correspondant
    if shp_file:
        renamed_shp_file = next((f for f in files if f.endswith('.shp')), None)
        suffix = identify_suffix(renamed_shp_file) if renamed_shp_file else 'unknown'
    else:
        suffix = ''

    # Obtenir les métadonnées après modification du nom
    metadata = get_metadata_for_file(base_name_modified, files)

    if metadata is None:
        return

    rename_file_group(files, metadata['prefix'], metadata['source'], metadata['year'], metadata['scale'], suffix)

def rename_files_with_new_base_name(base_name, base_name_modified, files, file_dir):
    """
    Renomme temporairement les fichiers avec le nouveau nom de base en prenant en compte toutes les extensions
    associées aux shapefiles (.shp, .shx, .dbf, .prj, .sbn, .sbx, .xml, etc.).
    """
    if base_name_modified != base_name:
        for i, file in enumerate(files):
            if file.endswith('.shp.xml'):
                new_file_name = f"{base_name_modified}.shp.xml"
            else:
                extension = os.path.splitext(file)[1]
                new_file_name = f"{base_name_modified}{extension}"

            new_file_path = os.path.join(file_dir, new_file_name)

            # Vérifier si le fichier cible existe déjà et l'ignorer si c'est le cas
            if os.path.exists(new_file_path):
                print(f"Le fichier '{new_file_path}' existe déjà. Ignoré.")
                continue  # Ne pas essayer de renommer si le fichier existe déjà

            try:
                os.rename(file, new_file_path)
                files[i] = new_file_path  # Mettre à jour la liste avec le nouveau chemin
                print(f"Renommage de '{file}' en '{new_file_path}'")
            except OSError as e:
                print(f"Erreur lors du renommage de '{file}' : {e}")

def ask_if_change_base_name(base_name_with_extension, base_name, files, file_dir):
    """
    Demande à l'utilisateur s'il souhaite modifier le nom de base d'un fichier.
    """
    change_base_name = input(f"Souhaitez-vous modifier le nom de base '{base_name_with_extension}' ? (o/n) [n] : ").lower()

    if change_base_name in ['o', 'oui']:
        base_name_modified_input = input(f"Entrez le nouveau nom de base pour '{base_name_with_extension}' : ").strip()
        if base_name_modified_input:
            print(f"Le nom de base '{base_name}' a été modifié en '{base_name_modified_input}'.")
            base_name = base_name_modified_input

    return base_name

def rename_file_group(files, prefix, source, year, scale, suffix):
    """
    Renomme un groupe de fichiers en fonction des métadonnées fournies et du suffixe détecté.
    """
    for file in files:
        if not is_file_already_renamed(file, dynamic_prefixes):
            new_name = apply_naming_convention(file, prefix, suffix, source, year, scale)

            if isinstance(new_name, str):
                os.rename(file, os.path.join(os.path.dirname(file), new_name))
                
                # Afficher uniquement le fichier .shp lors du renommage
                if file.endswith('.shp'):
                    log_info(f"Renommage de {file} en {new_name}")
                    print(f"Renommage de '{file}' en '{new_name}'")
            else:
                print(f"Erreur : Le nouveau nom pour le fichier '{file}' n'est pas valide : {new_name}")

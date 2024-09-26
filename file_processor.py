import os
from metadata_handler import get_metadata_for_file
from naming_convention import apply_naming_convention, identify_suffix
from utils import log_info, is_file_already_renamed

SUPPORTED_EXTENSIONS = ['.shp', '.shx', '.dbf', '.prj', '.sld', '.cpg', '.xml', '.shp.xml', '.qml', '.qlr', '.gpkg', '.json', '.geojson', '.csv', '.kmz', '.KMZ', '.kml', '.KML', '.dwg', '.DWG']

def collect_files_by_extension(folder, extensions):
    """
    Parcourt le dossier et regroupe les fichiers selon leur extension.
    Ignore les dossiers sans fichiers pris en charge.
    """
    file_groups = {}
    for root, dirs, files in os.walk(folder):
        valid_files = [file for file in files if any(file.endswith(ext) for ext in extensions)]
        if not valid_files:
            continue  # Ignorer les dossiers sans extensions valides

        for file in valid_files:
            base_name, ext = os.path.splitext(file)
            if base_name not in file_groups:
                file_groups[base_name] = []
            file_groups[base_name].append(os.path.join(root, file))  # Enregistre le chemin complet du fichier
    
    return file_groups

def process_files_in_directory(folder):
    """
    Traite les fichiers dans le dossier en utilisant les métadonnées pour le renommage.
    """
    # Collecter les fichiers par extension
    file_groups = collect_files_by_extension(folder, SUPPORTED_EXTENSIONS)

    # Si aucun fichier valide n'est trouvé, ne pas continuer
    if not file_groups:
        print(f"Aucun fichier valide trouvé dans le dossier {folder}.")
        return

    # Traiter chaque groupe de fichiers
    for base_name, files in file_groups.items():
        # Récupérer le dossier où se trouvent les fichiers
        file_dir = os.path.dirname(files[0])

        # Afficher le chemin du dossier avant de traiter le groupe
        print(f"Renommage des fichiers dans le dossier : {file_dir}")

        # Ignorer les fichiers déjà renommés
        if is_file_already_renamed(base_name):
            print(f"Le fichier '{base_name}' est déjà renommé selon la convention.")
            continue

        # Obtenir les métadonnées du fichier via metadata_handler
        metadata = get_metadata_for_file(base_name, files)

        # Si l'utilisateur choisit de ne pas renommer ou une erreur survient
        if metadata is None:
            continue

        # Trouver le fichier .shp pour obtenir le suffixe
        shp_file = next((f for f in files if f.endswith('.shp')), None)

        # Si un fichier .shp est trouvé, identifier le suffixe
        if shp_file:
            suffix = identify_suffix(shp_file)
        else:
            suffix = 'unknown'  # Si aucun .shp n'est trouvé, utiliser 'unknown'

        # Renommer chaque fichier du groupe avec le même suffixe
        rename_file_group(files, metadata['prefix'], metadata['source'], metadata['year'], metadata['scale'], suffix)

def rename_file_group(files, prefix, source, year, scale, suffix):
    """
    Renomme un groupe de fichiers en fonction des métadonnées et du suffixe détecté.
    """
    for file in files:
        # Ne renommer que si le fichier n'est pas déjà renommé
        if not is_file_already_renamed(file):
            # Appliquer le suffixe trouvé pour tout le groupe
            new_name = apply_naming_convention(file, prefix, suffix, source, year, scale)

            # Vérifier que new_name est bien une chaîne de caractères
            if isinstance(new_name, str):
                log_info(f"Renommage de {file} en {new_name}")
                print(f"Renommage de '{file}' en '{new_name}'")
                os.rename(file, os.path.join(os.path.dirname(file), new_name))
            else:
                print(f"Erreur : Le nouveau nom pour le fichier '{file}' n'est pas valide : {new_name}")


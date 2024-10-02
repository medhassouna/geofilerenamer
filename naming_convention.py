import os
import fiona
from utils import remove_accents_and_special_chars, split_into_segments, process_segments

# Liste des extensions généralement associées à un groupe de fichiers shapefile
SHAPEFILE_EXTENSIONS = ['.shp', '.shx', '.dbf', '.prj', '.sbn', '.sbx', '.sld', '.cpg', '.xml', '.shp.xml', '.qml', '.qlr', '.qpj', '.cst']

def apply_naming_convention(filename, prefix, suffix, source, year, scale):
    """
    Applique la convention de nommage au fichier selon le format :
    [prefix]_[suffix]_[nomFichierCamelCase]_[source]_[année].[extension].
    """
    # Extraire uniquement le nom de base du fichier, sans le chemin
    base_name = os.path.basename(filename)  # Nom de fichier avec extension
    base_name_no_ext = os.path.splitext(base_name)[0]  # Retirer l'extension

    # Gestion spécifique des fichiers .shp.xml
    if filename.endswith('.shp.xml'):
        base_name_no_ext = os.path.splitext(os.path.splitext(base_name)[0])[0]
        ext = '.shp.xml'
    else:
        ext = os.path.splitext(filename)[1].lower()

    # Si c'est un fichier GeoPackage, GeoJSON, CSV, KMZ, KML ou DWG, pas de suffixe
    if ext in ['.gpkg', '.json', '.geojson', '.csv', '.kmz', '.KMZ', '.kml', '.KML' '.dwg', '.DWG']:
        suffix = ''  # Pas de suffixe pour ces formats

    # Nettoyer et segmenter le nom du fichier
    cleaned_name = remove_accents_and_special_chars(base_name_no_ext)
    segments = split_into_segments(cleaned_name)
    camel_case_base = process_segments(segments)

    # Construire la nouvelle partie du nom de fichier sous forme de liste
    new_name_parts = [prefix, suffix, camel_case_base] if suffix else [prefix, camel_case_base]

    # Ajouter les métadonnées source, année, et échelle si elles sont spécifiées et ne sont pas égales à 'inconnue' ou vides
    if source and source.strip() and source != "inconnue":
        new_name_parts.append(source)
    if year and year.strip() and year != "inconnue":
        new_name_parts.append(year)
    if scale and scale.strip() and scale != "inconnue":
        new_name_parts.append(scale)

    # Joindre les parties avec un underscore et ajouter l'extension
    final_name = "_".join(new_name_parts)
    return f"{final_name}{ext}"


import fiona

def identify_suffix(shapefile):
    """
    Identifie le suffixe en fonction du type de géométrie contenu dans le fichier (Point, LineString, Polygon, etc.).
    Utilise Fiona pour lire les métadonnées du shapefile, y compris pour les géométries 3D (ex: PointZ, LineStringZ, PolygonZ, 3D types).
    """
    if shapefile.endswith('.shp'):
        try:
            # Ouvrir le fichier avec Fiona pour lire les métadonnées
            with fiona.open(shapefile, 'r') as src:
                # Vérifier si le fichier contient des entités
                if len(src) == 0:
                    print(f"Le fichier {shapefile} ne contient aucune entité.")
                    return "empty"
                
                # Récupérer le type de géométrie et supprimer "3D " si présent
                geom_type = src.schema['geometry'].replace("3D ", "")
                print(f"Type de géométrie détecté dans: {geom_type}")
                
                # Déterminer le suffixe en fonction du type de géométrie, y compris pour les géométries 3D (suffixe Z)
                if geom_type in ['Point', 'MultiPoint', 'PointZ', 'MultiPointZ']:
                    return "pt"
                elif geom_type in ['LineString', 'MultiLineString', 'LineStringZ', 'MultiLineStringZ']:
                    return "line"
                elif geom_type in ['Polygon', 'MultiPolygon', 'PolygonZ', 'MultiPolygonZ']:
                    return "poly"
                else:
                    print(f"Géométrie non supportée : {geom_type}")
                    return "unknown"
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {shapefile}: {e}")
            return "unknown"
    return ""  # Si le fichier n'est pas un shapefile

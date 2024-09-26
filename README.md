GeoFileRenamer
GeoFileRenamer est un outil interactif de renommage en ligne de commande pour les fichiers géospatiaux couramment utilisés dans les Systèmes d'Information Géographique (SIG), tels que les shapefiles, GeoPackages, KML, KMZ, DWG, etc. Ce programme aide à normaliser les noms de fichiers tout en intégrant les métadonnées essentielles comme la source, l'année, et l'échelle des données. Grâce à son fonctionnement intuitif, l'utilisateur peut interagir avec l'outil via des prompts dans le terminal pour valider ou ajuster ces informations.

Fonctionnalités principales
1. Renommage automatisé selon une convention de nommage
L'outil renomme les fichiers selon une convention de nommage stricte et configurable, facilitant ainsi leur gestion et leur identification. La convention suit le format suivant :

css
Copy code
[prefix]_[suffix]_[nomFichierCamelCase]_[source]_[année]_[échelle].[extension]
Exemple :

bati_poly_batiment_bdtopo_2023_25K.shp
veg_pt_arbre_bdtopo_2023_1K.geojson
hydro_line_riviere_bdtopo_2023_10K.dwg
2. Détection automatique des suffixes géométriques
L'outil détecte automatiquement le type de géométrie (point, ligne, polygone, etc.) pour les fichiers shapefile (.shp) en utilisant la bibliothèque Fiona.
Les suffixes suivants sont appliqués en fonction de la géométrie détectée :
pt : pour les points (Point, MultiPoint)
line : pour les lignes (LineString, MultiLineString)
poly : pour les polygones (Polygon, MultiPolygon)
unknown : pour les types de géométrie non reconnus.
3. Prise en charge des fichiers géospatiaux courants
En plus des shapefiles, GeoFileRenamer prend en charge d'autres formats géospatiaux tels que :

GeoJSON (.json)
GeoPackage (.gpkg)
KML et KMZ (.kml, .kmz)
DWG (.dwg)
4. Gestion des métadonnées utilisateur
L'utilisateur peut interagir avec l'outil pour fournir des métadonnées (source, année, échelle) lors du renommage des fichiers.
Les dernières valeurs utilisées pour ces métadonnées sont proposées par défaut, ce qui permet de gagner du temps lors du traitement de groupes de fichiers similaires.
5. Validation des entrées utilisateur
L'outil inclut des validations strictes pour s'assurer que les informations saisies par l'utilisateur respectent les formats attendus :

Année : Doit être au format YYYY. Exemple : 2023
Échelle : Doit être au format valide, tel que 10K, 200K, 1K, ou 2000K.
Si l'utilisateur tente d'entrer une valeur non valide, l'outil redemande l'entrée jusqu'à ce qu'une valeur correcte soit fournie. Si l'utilisateur ne fournit pas de valeur, l'outil propose la dernière valeur entrée ou lui permet d'ignorer cette métadonnée.

6. Sauvegarde dynamique des mots-clés
Lorsqu'un fichier ne correspond à aucun des mots-clés connus pour un préfixe donné, l'outil propose d'ajouter un nouveau mot-clé au fichier metadata.json pour une utilisation future.
Les mots-clés sont enregistrés et rechargés à chaque exécution pour garantir une évolution continue du système de classification.
7. Interface interactive pour l'utilisateur
GeoFileRenamer est conçu pour être interactif, et chaque étape du processus de renommage est contrôlée par l'utilisateur :

Validation ou ajustement des préfixes.
Saisie ou réutilisation des métadonnées.
Ajout de nouveaux mots-clés au besoin.
Validations intégrées
Validation de l'année
L'utilisateur est invité à entrer une année au format YYYY. L'outil vérifie que l'entrée est une valeur à 4 chiffres représentant une année valide.

Exemple :

bash
Copy code
Veuillez entrer l'année des données (format: YYYY) ou appuyez sur Entrée pour garder l'ancienne valeur : 2023
Si une entrée non valide est fournie, l'utilisateur est invité à essayer à nouveau.

Validation de l'échelle
L'échelle doit être fournie dans un format précis, tel que 10K, 200K, 1K, 2000K. L'outil vérifie que l'entrée respecte ce format.

Exemple :

bash
Copy code
Veuillez entrer l'échelle des données (ex: 10K, 25K) ou appuyez sur Entrée pour garder l'ancienne valeur : 25K
En cas de saisie incorrecte, l'utilisateur est invité à réessayer.

Validation de la source
L'utilisateur peut entrer une source ou choisir de l'ignorer en tapant n. L'outil ne force pas l'entrée de la source, mais encourage l'utilisateur à fournir cette information si disponible.

Exemple :

bash
Copy code
Veuillez entrer la source (ex: bdtopo) ou appuyez sur Entrée pour réutiliser 'None' ou tapez n pour ignorer : bdtopo
Comment utiliser GeoFileRenamer
Lancer l'application : Exécutez le programme en utilisant Python.

bash
Copy code
python main.py
Renommer les fichiers : Suivez les instructions interactives pour renommer vos fichiers. L'outil va vous demander de valider ou d'ajuster les métadonnées pour chaque fichier.

Ajout de mots-clés : Si un mot-clé est manquant, l'outil vous proposera de l'ajouter automatiquement à la liste des mots-clés dans metadata.json.

Personnalisation
Modifier les mots-clés
Le fichier metadata.json stocke les mots-clés associés à chaque catégorie de fichiers. Ce fichier peut être édité manuellement ou enrichi dynamiquement via l'interface utilisateur de GeoFileRenamer.

Adapter la convention de nommage
Si la convention de nommage doit être modifiée, il suffit de modifier la fonction apply_naming_convention dans le fichier naming_convention.py. Cela vous permet d'adapter la structure des noms de fichiers aux besoins spécifiques de votre projet.

Contribuer
Toutes les contributions sont les bienvenues ! Que vous ayez des idées pour de nouvelles fonctionnalités, des corrections de bugs ou des suggestions d'amélioration, n'hésitez pas à ouvrir une issue ou une pull request sur GitHub.
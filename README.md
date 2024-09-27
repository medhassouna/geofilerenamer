GeoFileRenamer

GeoFileRenamer is a Python-based tool designed to efficiently rename geographic files following a consistent naming convention. It supports a variety of geospatial file formats and ensures data is named in a structured and meaningful way.

Features

- Supports multiple geospatial formats: Renames files like .shp, .json, .csv, .gpkg, .kmz, .kml, .dwg, and more.
- Handles grouped shapefile components: Deals with shapefile extensions like .shp, .shx, .dbf, .prj, etc., as a single entity.
- Automatic file type detection: Identifies geometry types like Point, Line, Polygon, and assigns the appropriate suffix.
- Prefix detection based on folders and keywords: Detects and assigns prefixes automatically based on the folder structure or keyword matching.

User input for metadata: Allows users to input metadata like:
Source: Optional with an option to skip.
Year: Must be a 4-digit year (e.g., YYYY).
Scale: Must follow a format like 10K, 200K, 1K, etc.

Keyword management: If a relevant keyword is missing, users can add it dynamically during file renaming.

File normalization: File names are normalized using camelCase.

Interactive command-line tool: Allows users to interactively confirm operations, update filenames, and provide metadata through the command-line interface (CLI).

Installation

Clone the repository:
bash
Copy code
git clone https://github.com/medhassouna/geofilerenamer.git
cd geofilerenamer
Install dependencies:
Create a requirements.txt file and run the following command to install the necessary dependencies:

bash
Copy code
pip install -r requirements.txt
If no external dependencies are required, this step can be omitted.

Usage
Run the tool by executing the following command:

bash
Copy code
python main.py
The tool scans the specified directory for valid geographic files and prompts the user to confirm renaming for each file.

Example Command-line Interactions
When a file is detected, the tool will prompt the user with an option to rename:

bash
Copy code
Souhaitez-vous renommer le fichier [filename]? (o/n) [o] :
Then, it will ask for metadata like the source, year, and scale:

bash
Copy code
Veuillez entrer la source (ex: bdtopo) ou appuyez sur Entrée pour ignorer :
Veuillez entrer l'année des données (format: YYYY) ou appuyez sur Entrée pour ignorer :
Veuillez entrer l'échelle des données (ex: 10K, 25K) ou appuyez sur Entrée pour ignorer :

Example Workflow:

The tool scans a directory for files with supported extensions.
It processes each file (or file group in the case of shapefiles), checking if they already conform to the naming convention.
Users are asked to confirm or modify the detected prefix, metadata, or even file base names.
Files are renamed according to the provided metadata and naming convention.
File Naming Convention
The naming convention standardizes file names as follows:

css
Copy code
[prefix]_[suffix]_[filenameCamelCase]_[source]_[year].[extension]
Where:

Prefix: Detected based on the folder or file keywords (e.g., trans, hydro, zone).
Suffix: Detected based on file geometry for shapefiles (pt, line, poly), or omitted for non-shapefiles.
Filename in camelCase: Converts the original file name into camelCase format.
Source: Provided by the user during renaming.
Year: A 4-digit year (e.g., 2023).
Scale: Optional, must follow the format like 10K, 200K.
Contributing

We welcome contributions! To contribute:

Fork the repository.
Create a new branch for your feature (git checkout -b feature/your-feature-name).
Commit your changes (git commit -am 'Add some feature').
Push to the branch (git push origin feature/your-feature-name).
Open a pull request.

License
This project is licensed under the MIT License – see the LICENSE file for details.
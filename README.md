# GeoFileRenamer

**GeoFileRenamer** is a Python-based tool designed to efficiently rename geographic files following a consistent naming convention. It supports a variety of geospatial file formats and ensures data is named in a structured and meaningful way.

## Features

- Supports renaming of geospatial files such as `.shp`, `.json`, `.csv`, `.gpkg`, `.kmz`, `.kml`, and `.dwg`.
- Handles shapefiles with grouped components (e.g., `.shp`, `.shx`, `.dbf`, `.prj`, etc.).
- Automatic detection of file types (e.g., `Point`, `Line`, `Polygon`) and appropriate suffix assignment.
- Supports prefix detection based on folder names and keywords.
- Allows user to input metadata like source, year, and scale with validation:
  - **Year** must be in the format `YYYY`.
  - **Scale** must be in the format like `10K`, `200K`, `1K`.
- Keyword management: users can add new keywords to the system when renaming files.
- File extension and naming are normalized using `camelCase`.
- No GUI – pure command-line interaction for flexibility and simplicity.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/medhassouna/geofilerenamer.git
   cd geofilerenamer
Install dependencies:

If your project has dependencies, list them in a requirements.txt file and include this step to install them:

bash
Copy code
pip install -r requirements.txt
If there are no external dependencies, you can omit this step.

Usage
Run the script using Python in the command line:

bash
Copy code
python main.py
Command-line interactions:
When renaming files, the tool will ask for user input to confirm the operation and allow metadata entry (source, year, scale).

bash
Copy code
Souhaitez-vous renommer le fichier [filename]? (o/n) [o] : 
The source, year, and scale prompts include validation, and the user can skip entering values by pressing Enter.

bash
Copy code
Veuillez entrer la source (ex: bdtopo) ou appuyez sur Entrée pour ignorer : 
Veuillez entrer l'année des données (format: YYYY) ou appuyez sur Entrée pour ignorer : 
Veuillez entrer l'échelle des données (ex: 10K, 25K) ou appuyez sur Entrée pour ignorer :
Example workflow:
The tool scans a directory for valid files.
It then processes each file, checking whether it follows the naming conventions.
Users can validate or change the detected prefix and add new keywords.
Files are renamed according to the detected or provided metadata.
File Naming Convention
The tool uses a specific naming convention to standardize the names of geographic files:

css
Copy code
[prefix]_[suffix]_[filenameCamelCase]_[source]_[year]_[scale].[extension]
Prefix: Detected based on folder or file keywords (e.g., trans, hydro, zone).
Suffix: Detected based on file geometry (e.g., pt, line, poly).
Filename in camelCase: Converts the original file name into camelCase.
Source: Provided by the user.
Year: Must be a 4-digit year (YYYY).
Scale: Optional, must follow the format like 10K, 200K.
Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new feature branch (git checkout -b feature/your-feature-name).
Commit your changes (git commit -am 'Add some feature').
Push the branch (git push origin feature/your-feature-name).
Open a pull request.
License
This project is licensed under the MIT License – see the LICENSE file for details.
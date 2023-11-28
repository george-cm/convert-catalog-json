# covert_catalog_json

Convert a AEM catalog.json file to csv. Probably not useful for anyone else.

Saves the products and categories in two csv files.

## Installation

Install in a virtual environment using:

```sh
python -m pip install "git+https://github.com/george-cm/convert-catalog-json.git#egg=convert_catalog_json"
```

## Usage

```sh
usage: convert_catalog_json [-h] [--outputdir OUTPUTDIR] [--version] jsonfile

Convert AEM catalog.json file to csv. Probably not useful for anyone else.

positional arguments:
  jsonfile              Path to catalog.json file

options:
  -h, --help            show this help message and exit
  --outputdir OUTPUTDIR, -o OUTPUTDIR
                        Path to folder in which to save the csv files. If not provided the csv files will be
                        saved in the same folder as the input file.
  --version, -V         show program's version number and exit
```

"""Convert AEM catalog.json file to csv. Probably not useful for anyone else."""
import csv
import json
from pathlib import Path
import argparse
from collections import deque
from typing import TypeAlias

__version__ = "v1.0"

CategoryItem: TypeAlias = dict[str, str | int | list["CategoryItem"]]


def main():
    """Main function."""
    parser = argparse.ArgumentParser(prog="convert_catalog_json", description=__doc__)
    parser.add_argument("jsonfile", type=str, help="Path to catalog.json file")
    parser.add_argument(
        "--outputdir",
        "-o",
        type=str,
        help="Path to folder in which to save the csv files. "
        "If not provided the csv files will be saved in the same folder as the input file.",
    )
    parser.add_argument(
        "--version", "-V", action="version", version="%(prog)s " + __version__
    )
    args: argparse.Namespace = parser.parse_args()
    jsonfile_path = Path(args.jsonfile)
    if not jsonfile_path.exists():
        raise IOError(f"File {jsonfile_path} does not exist.")
    if not jsonfile_path.is_file():
        raise IOError(f"File {jsonfile_path} is not a file.")

    csvfolder_path = Path(args.outputdir) if args.outputdir else jsonfile_path.parent
    if not csvfolder_path.exists():
        raise IOError(f"Directory {csvfolder_path} does not exist.")

    products: list[CategoryItem]
    categories: list[CategoryItem]

    products, categories = convert_json_to_csv(jsonfile_path, csvfolder_path)
    products_file: Path = csvfolder_path / (jsonfile_path.stem + "_products.csv")
    categories_file: Path = csvfolder_path / (jsonfile_path.stem + "_categories.csv")
    if len(products) > 0:
        save_to_csv(products, products_file)
    if len(categories) > 0:
        save_to_csv(categories, categories_file)

    print(f"Converted {len(products)} products and {len(categories)} categories.")


def convert_json_to_csv(
    jsonfile_path: Path | str, csvfolder_path: Path | str
) -> tuple[list[CategoryItem], list[CategoryItem]]:
    """Converts an AEM catalog.json file to csv."""
    if not isinstance(jsonfile_path, Path):
        jsonfile_path = Path(jsonfile_path)
    if not isinstance(csvfolder_path, Path):
        csvfolder_path = Path(csvfolder_path)
    with jsonfile_path.open("r", encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)

    items_deque: deque = deque()
    items_deque.extend(data["catalog"])
    products: list[CategoryItem] = []
    categories: list[CategoryItem] = []

    while len(items_deque) > 0:
        category_item: CategoryItem = items_deque.popleft()
        categories.append(
            {
                "structure_group_id": category_item["pimId"],
                "name": category_item["name"],
                "nameEn": category_item["nameEn"],
                "node_type": category_item["nodeType"],
                "level": category_item["level"],
                "parent_id": category_item["parentId"],
            }
        )
        if "products" in category_item:
            for product in category_item["products"]:  # type: ignore
                products.append(
                    {
                        "pim_id": product["pimid"],
                        "product_no": product["productNo"],
                        "name": product["productName"],
                        "nameEn": product["productNameEn"],
                        "category_id": category_item["pimId"],
                        "category_name": category_item["name"],
                        "category_nameEn": category_item["nameEn"],
                    }
                )
        if "subCategories" in category_item:
            items_deque.extend(category_item["subCategories"])  # type: ignore

    return products, categories


def save_to_csv(items_list: list[CategoryItem], csvfile: Path) -> None:
    """Saves a list of categories or products to a csv file."""
    with csvfile.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=items_list[0].keys(), dialect="excel")
        writer.writeheader()
        writer.writerows(items_list)


if __name__ == "__main__":
    main()

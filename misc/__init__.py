import json
import os
from typing import Optional

from misc.model import PackageType

# Paths
API_BASE_URL = "https://packagist.org"
ROOT_DIR = os.getcwd()
DATA_DIR = os.path.join(ROOT_DIR, 'dataset')


def load_json_dataset(path: str) -> list:
    print(f"🟢 Loading JSON dataset from {path}")
    with open(os.path.join(DATA_DIR, path), "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_dataset(data: list, path: str) -> None:
    print(f"🟢 Saving JSON dataset to {path}")

    os.makedirs(os.path.join(DATA_DIR, os.path.dirname(path)), exist_ok=True)

    with open(os.path.join(DATA_DIR, path), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))


def load_packages_list(package_type: PackageType) -> list:
    return load_json_dataset(f"{package_type.value}.json")['packageNames']


def package_info_exists(package_name: str) -> bool:
    vendor, package = package_name.split("/", 1)
    return os.path.exists(os.path.join(DATA_DIR, f"packages/{vendor}/{package}.json"))


def load_package_info(package_name: str) -> Optional[dict]:
    if not package_info_exists(package_name):
        return None

    vendor, package = package_name.split("/", 1)
    return load_json_dataset(f"packages/{vendor}/{package}.json")['package']

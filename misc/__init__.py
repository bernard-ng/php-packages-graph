import json
import os

# Paths
API_BASE_URL = "https://packagist.org"
ROOT_DIR = os.getcwd()
DATA_DIR = os.path.join(ROOT_DIR, 'dataset')

# Neo4j connection settings
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"


def load_json_dataset(path: str) -> list:
    print(f">> Loading JSON dataset from {path}")
    with open(os.path.join(DATA_DIR, path), "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_dataset(data: list, path: str) -> None:
    print(f">> Saving JSON dataset to {path}")
    with open(os.path.join(DATA_DIR, path), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

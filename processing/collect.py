import requests
import time

from misc import API_BASE_URL, save_json_dataset, DATA_DIR, ROOT_DIR
from misc.model import PackageType


def fetch_packages_list() -> None:
    """Fetches package lists from Packagist and stores them in JSON files."""

    for package_type in PackageType:
        url = f"{API_BASE_URL}/packages/list.json?type={package_type.value}"

        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            data = response.json()
            save_json_dataset(data, f"{package_type.value}.json")

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to fetch {package_type.value}: {e}")

        time.sleep(1)


def fetch_package_info(package_name: str) -> None:
    """Fetches package information from Packagist."""
    url = f"{API_BASE_URL}/packages/{package_name}.json"
    vendor, package = package_name.split("/", 1)

    # Check if the package is already fetched
    if f"/packages/{vendor}/{package}.json" in DATA_DIR.iterdir():
        print(f"✅ {package_name} is already fetched.")
        return

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        save_json_dataset(data, f"/packages/{vendor}/{package}.json")

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch {package_name}: {e}")

    time.sleep(1)


if __name__ == "__main__":
    fetch_packages_list()

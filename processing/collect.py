import time

import requests
from tqdm import tqdm

from misc import API_BASE_URL, save_json_dataset, DATA_DIR, load_json_dataset
from misc.model import PackageType


def fetch_packages_list() -> None:
    """
    Fetches a list of packages from Packagist for each package type and stores it in a JSON file.

    Returns:
        None
    """
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


def fetch_packages_info() -> None:
    """
    Fetches detailed information about all packages from Packagist and stores it in JSON files.

    Returns:
        None
    """
    for package_type in PackageType:
        packages = load_json_dataset(f"{package_type.value}.json")['packageNames']

        for package_name in tqdm(packages, desc=f"Fetching {package_type.value} packages"):
            fetch_package_info(package_name)
            time.sleep(0.2)

        print(f"✅ {len(packages)} {package_type.value} packages fetched.")


def fetch_package_info(package_name: str) -> None:
    """
    Fetches detailed information about a specific package from Packagist and stores it in a JSON file.

    Args:
        package_name (str): The name of the package in the format 'vendor/package'.

    Returns:
        None
    """
    url = f"{API_BASE_URL}/packages/{package_name}.json"
    vendor, package = package_name.split("/", 1)

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
        return


if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1. Fetch packages list")
        print("2. Fetch packages info")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            fetch_packages_list()
        elif choice == "2":
            fetch_packages_info()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

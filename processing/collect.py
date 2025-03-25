import argparse
from typing import Optional

import requests

from misc import API_BASE_URL, save_json_dataset, load_packages_list, package_info_exists
from misc.model import PackageType


def fetch_packages_list(package_type: Optional[str] = None) -> None:
    for pt in PackageType if package_type is None else [PackageType(package_type)]:
        url = f"{API_BASE_URL}/packages/list.json?type={pt.value}"

        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            data = response.json()
            save_json_dataset(data, f"{pt.value}.json")

        except requests.exceptions.RequestException as e:
            print(f"🔴 Failed to fetch {pt.value} packages list : {e}")


def fetch_packages_info(package_type: Optional[str] = None, force_update: bool = False) -> None:
    for pt in PackageType if package_type is None else [PackageType(package_type)]:
        packages = load_packages_list(pt)

        for package_name in packages:
            fetch_package_info(package_name, force_update)

        print(f"🟢 {len(packages)} {pt.value} packages fetched.")


def fetch_package_info(package_name: str, force_update: bool = False) -> None:
    url = f"{API_BASE_URL}/packages/{package_name}.json"
    vendor, package = package_name.split("/", 1)

    if package_info_exists(package_name) and not force_update:
        print(f"🟡 {package_name} is already fetched (use --force-update to update)")
        return

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        save_json_dataset(data, f"packages/{vendor}/{package}.json")

    except requests.exceptions.RequestException as e:
        print(f"🔴 Failed to fetch {package_name} info : {e}")
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch packages from Packagist")
    parser.add_argument("--fetch-list", action="store_true", help="Fetch packages list")
    parser.add_argument("--fetch-info", action="store_true", help="Fetch packages info")
    parser.add_argument("--package-type", type=str, help="Specify the package type")
    parser.add_argument("--force-update", action="store_true", help="Force update package info")

    args = parser.parse_args()

    if args.fetch_list:
        fetch_packages_list(args.package_type)
    elif args.fetch_info:
        fetch_packages_info(args.package_type, args.force_update)
    else:
        print("🔴 No valid option provided. Use --fetch-list or --fetch-info.")

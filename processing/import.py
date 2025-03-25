import argparse
from typing import List

from neo4j import GraphDatabase
from tqdm import tqdm

from misc import load_packages_list
from misc.database import neo4j_driver
from misc.model import PackageType


def setup_packages_constraints(driver: GraphDatabase.driver) -> None:
    with driver.session() as session:
        session.run("CREATE CONSTRAINT unique_vendor_name IF NOT EXISTS FOR (v:Vendor) REQUIRE v.name IS UNIQUE")
        session.run("CREATE CONSTRAINT unique_package_fullname IF NOT EXISTS FOR (p:Package) REQUIRE p.full_name IS UNIQUE")
        print("🟢 Database constraints set up")


def clear_database(driver: GraphDatabase.driver) -> None:
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        print("🟢 Database cleared.")


def create_package_nodes(driver: GraphDatabase.driver, package_names: List[str], package_type: PackageType) -> None:
    with driver.session() as session:
        for package_name in tqdm(package_names, desc=f"Creating {package_type.value} package nodes"):
            vendor, package = package_name.split("/", 1)

            try:
                query = """
                MERGE (v:Vendor {name: $vendor})
                MERGE (p:Package {name: $package, vendor: $vendor, full_name: $package_name, type: $type})
                MERGE (v)-[:OWNS]->(p);
                """
                session.run(query, vendor=vendor, package=package, package_name=package_name, type=package_type.value)
            except Exception as e:
                print(f"🔴 Failed to create node for {package_name}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import packages into Neo4j")
    parser.add_argument("--skip-clear", action="store_true", help="Skip clearing the database")
    args = parser.parse_args()

    if not args.skip_clear:
        clear_database(neo4j_driver)
        setup_packages_constraints(neo4j_driver)
    else:
        print("🟡 Skipping database clearing.")

    for p_type in PackageType:
        packages = load_packages_list(p_type)
        print(f"🟢 {len(packages)} {p_type.value} packages found.")

        create_package_nodes(neo4j_driver, packages, p_type)

    neo4j_driver.close()
    print("🟢 Packages importation completed !")

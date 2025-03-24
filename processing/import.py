import argparse
from typing import List

from neo4j import GraphDatabase
from tqdm import tqdm

from misc import load_json_dataset, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from misc.model import PackageType


def setup_constraints(driver: GraphDatabase.driver) -> None:
    """
    Sets up constraints in the Neo4j database.
    Ensures a unique constraint on packages to avoid duplicates.

    Args:
        driver (GraphDatabase.driver): The Neo4j driver instance.

    Returns:
        None
    """
    with driver.session() as session:
        session.run("CREATE CONSTRAINT unique_vendor_name IF NOT EXISTS FOR (v:Vendor) REQUIRE v.name IS UNIQUE")
        session.run("CREATE CONSTRAINT unique_package_fullname IF NOT EXISTS FOR (p:Package) REQUIRE p.full_name IS UNIQUE")
        print("✅ Constraints set up.")


def clear_database(driver: GraphDatabase.driver) -> None:
    """
    Clears all nodes and relationships in the Neo4j database.

    Args:
        driver (GraphDatabase.driver): The Neo4j driver instance.

    Returns:
        None
    """
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        print("✅ Database cleared.")


def create_package_nodes(driver: GraphDatabase.driver, package_names: List[str], package_type: PackageType) -> None:
    """
    Creates package nodes in the Neo4j database.

    Args:
        driver (GraphDatabase.driver): The Neo4j driver instance.
        package_names (List[str]): A list of package names in the format 'vendor/package'.
        package_type (PackageType): The type of the package.

    Returns:
        None
    """
    with driver.session() as session:
        for package_name in tqdm(package_names, desc=f"Creating {package_type.value} package nodes"):
            vendor, package = package_name.split("/", 1)

            try:
                query = """
                MERGE (v:Vendor {name: $vendor})
                MERGE (p:Package {name: $package, full_name: $package_name, type: $type})
                MERGE (v)-[:OWNS]->(p);
                """
                session.run(query, vendor=vendor, package=package, package_name=package_name, type=package_type.value)
            except Exception as e:
                continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import packages into Neo4j")
    parser.add_argument("--skip-clear", action="store_true", help="Skip clearing the database")
    args = parser.parse_args()

    neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    if args.skip_clear:
        print("⚠️ Skipping database clearing.")
    else:
        clear_database(neo4j_driver)
        setup_constraints(neo4j_driver)

    for p_type in PackageType:
        packages = load_json_dataset(f"{p_type.value}.json")['packageNames']
        print(f">> {len(packages)} {p_type.value} packages found.")

        create_package_nodes(neo4j_driver, packages, p_type)

    neo4j_driver.close()
    print("✅ Import completed!")

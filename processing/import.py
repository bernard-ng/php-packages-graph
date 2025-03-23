from typing import List

from neo4j import GraphDatabase
from tqdm import tqdm

from misc import load_json_dataset, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from misc.model import PackageType


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

            query = """
            MERGE (v:Vendor {name: $vendor})
            MERGE (p:Package {name: $package, package: $package, type: $type})
            MERGE (v)-[:OWNS]->(p);
            """
            session.run(query, vendor=vendor, name=package, package=package_name, type=package_type.value)


if __name__ == "__main__":
    neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    confirm = input("Are you sure you want to clear the database? (yes/no): ")
    if confirm.lower() == "yes":
        clear_database(neo4j_driver)
    else:
        print("⚠️ Skipping database clearing.")

    for p_type in PackageType:
        packages = load_json_dataset(f"{p_type.value}.json")['packageNames']
        print(f">> {len(packages)} {p_type.value} packages found.")

        create_package_nodes(neo4j_driver, packages, p_type)

    neo4j_driver.close()
    print("✅ Import completed!")

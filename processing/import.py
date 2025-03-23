from neo4j import GraphDatabase
from misc import load_json_dataset, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from tqdm import tqdm

from misc.model import PackageType


def clear_database(driver) -> None:
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        print("✅ Database cleared.")


def create_package_nodes(driver, package_names, package_type: PackageType) -> None:
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
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    clear_database(driver)

    for p_type in PackageType:
        packages = load_json_dataset(f"{p_type.value}.json")['packageNames']
        print(f">> {len(packages)} {p_type.value} packages found.")

        create_package_nodes(driver, packages, p_type)

    driver.close()
    print("✅ Import completed!")

import argparse

from neo4j import GraphDatabase

from misc import load_packages_list, PackageType, load_package_info
from misc.database import neo4j_driver
from misc.model import Package


def add_package_info(driver: GraphDatabase.driver, package: Package) -> None:
    query = """
    MATCH (p:Package {full_name: $package_name})
    SET p += {
        description: $description,
        published_at: datetime($published_at),
        updated_at: datetime($updated_at),
        licenses: $licenses,
        versions: $versions,
        authors: $authors,
        repository: $repository,
        github_stars: $github_stars,
        github_watchers: $github_watchers,
        github_forks: $github_forks,
        github_open_issues: $github_open_issues,
        language: $language,
        abandoned: $abandoned,
        downloads: $downloads
    }
    """

    params = {
        "package_name": package.name,
        "description": package.description,
        "published_at": package.time.isoformat(),
        "updated_at": package.last_updated_time().isoformat(),
        "licenses": package.aggregate_licenses(),
        "versions": package.aggregate_versions(),
        "authors": package.aggregate_authors(),
        "repository": str(package.repository),
        "github_stars": package.github_stars,
        "github_watchers": package.github_watchers,
        "github_forks": package.github_forks,
        "github_open_issues": package.github_open_issues,
        "language": package.language,
        "abandoned": package.abandoned,
        "downloads": package.downloads.total
    }

    with driver.session() as session:
        session.run(query, **params)

    print(f"🟢 Info for {package.name} added.")


def add_package_dependencies(driver: GraphDatabase.driver, package: Package) -> None:
    relationships = {
        "REQUIRES": package.aggregate_require(),
        "DEV_REQUIRES": package.aggregate_require_dev(),
        "CONFLICTS": package.aggregate_conflict(),
        "PROVIDES": package.aggregate_provide(),
        "REPLACES": package.aggregate_replace(),
        "SUGGESTS": package.aggregate_suggest(),
    }

    queries_with_params = [
        (
            f"""
            MATCH (p:Package {{full_name: $package_name}})
            MATCH (d:Package {{full_name: $dependency_name}})
            MERGE (p)-[:{rel_type}]->(d)
            """,
            {"package_name": package.name, "dependency_name": dependency}
        )
        for rel_type, dependencies in relationships.items()
        for dependency in dependencies
    ]

    with driver.session() as session:
        session.execute_write(lambda tx: [
            tx.run(query, params) for query, params in queries_with_params
        ])

    print(f"🟢 Dependencies for {package.name} added.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add packages info and dependencies to Neo4j")
    parser.add_argument("--add-info", action="store_true", help="Update packages info")
    parser.add_argument("--add-deps", action="store_true", help="Update packages dependencies")
    parser.add_argument("--package-type", type=str, help="Specify the package type")

    args = parser.parse_args()
    selected_types = [PackageType(args.package_type)] if args.package_type else PackageType

    for package_type in selected_types:
        packages = load_packages_list(package_type)
        success, fail = 0, 0

        for package_name in packages:
            try:
                p = Package(**load_package_info(package_name))

                if args.add_info:
                    add_package_info(neo4j_driver, p)
                if args.add_relation:
                    add_package_dependencies(neo4j_driver, p)

                success += 1

            except Exception as e:
                print(f"🔴 Failed to define info for {package_name}: {e}")
                fail += 1

        neo4j_driver.close()
        print(f"🟢 Processed {success}/{len(packages)} {package_type.value} packages successfully ({fail} failed).")

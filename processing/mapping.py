import argparse

from neo4j import GraphDatabase

from misc import load_packages_list, load_package_info
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
        downloads: $downloads,
        type: $type,
        has_stable_release: $has_stable_release,
        is_custom_type: $is_custom_type
    }
    """

    params = {
        "package_name": package.name,
        "description": package.description,
        "published_at": package.time.isoformat(),
        "repository": str(package.repository),
        "github_stars": package.github_stars,
        "github_watchers": package.github_watchers,
        "github_forks": package.github_forks,
        "github_open_issues": package.github_open_issues,
        "language": package.language,
        "abandoned": package.abandoned,
        "downloads": package.downloads.total,
        "type": package.type,
        "updated_at": package.last_updated_time().isoformat(),
        "licenses": package.aggregate_licenses(),
        "versions": package.aggregate_versions(),
        "authors": package.aggregate_authors(),
        "has_stable_release": package.has_stable_version(),
        "is_custom_type": package.is_custom_type()
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

    args = parser.parse_args()
    packages = load_packages_list()
    success, fail = 0, 0

    if not args.add_info and not args.add_deps:
        print("🔴 No valid option provided. Use --add-info or --add-deps.")
        exit(1)

    for package_name in packages:
        try:
            p = Package(**load_package_info(package_name))

            if args.add_info:
                add_package_info(neo4j_driver, p)
            if args.add_deps:
                add_package_dependencies(neo4j_driver, p)

            success += 1

        except Exception as e:
            print(f"🔴 Failed to define info for {package_name}: {e}")
            fail += 1

    neo4j_driver.close()
    print(f"🟢 Processed {success}/{len(packages)} packages successfully ({fail} failed).")

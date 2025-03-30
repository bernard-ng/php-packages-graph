// Distribution of Packages by License
MATCH (p:Package)
UNWIND p.licenses AS license
RETURN license, COUNT(p) AS package_count
ORDER BY package_count DESC;

// Most Common License(s)
MATCH (p:Package)
UNWIND p.licenses AS license
RETURN license, COUNT(p) AS count
ORDER BY count DESC
LIMIT 1;

// Top Required Packages
MATCH (:Package)-[:REQUIRES]->(p:Package)
RETURN p.full_name AS package, COUNT(*) AS times_required
ORDER BY times_required DESC
LIMIT 100;

MATCH (:Package)-[:DEV_REQUIRES]->(p:Package)
RETURN p.full_name AS package, COUNT(*) AS times_required
ORDER BY times_required DESC
LIMIT 100;

// Packages That Are Both Required and Dev Required
MATCH (p:Package)
OPTIONAL MATCH (:Package)-[:REQUIRES]->(p)
WITH p, COUNT(*) AS required_count
OPTIONAL MATCH (:Package)-[:DEV_REQUIRES]->(p)
WITH p, required_count, COUNT(*) AS dev_required_count
WHERE required_count > 0 AND dev_required_count > 0
RETURN p.full_name, required_count, dev_required_count
ORDER BY required_count DESC, dev_required_count DESC
LIMIT 10;

// Top downloaded packages
MATCH (p:Package)
WHERE p.total_downloads IS NOT NULL
RETURN p.full_name AS package, p.total_downloads AS downloads
ORDER BY downloads DESC
LIMIT 10;

// Average number of authors per package
MATCH (p:Package)
WITH count(p) AS total_packages, avg(size(p.authors)) AS avg_authors
RETURN avg_authors;

// Packages by year of initial release and type
MATCH (p:Package)
WHERE p.type = 'project'
WITH date(p.published_at).year AS year, count(p) AS package_count
RETURN year, package_count
ORDER BY year ASC;

// Oldest packages still maintained
MATCH (p:Package)
WHERE (p.abandoned IS NULL OR p.abandoned = false)
  AND p.published_at IS NOT NULL
  AND p.updated_at IS NOT NULL
WITH DISTINCT p,
     duration.between(datetime(p.published_at), datetime(p.updated_at)) AS lifespan
ORDER BY lifespan.years DESC
LIMIT 10
RETURN DISTINCT p.full_name AS package_name, p.published_at, p.updated_at, lifespan.days

// Find all packages owned by the vendor "symfony"
MATCH (v:Vendor)-[:OWNS]->(p:Package)
  WHERE v.name = 'symfony'
RETURN p.package;

// Find all packages that depend on the package "symfony/console"
MATCH (p:Package)-[:REQUIRES]->(d:Package)
  WHERE d.package = 'symfony/console'
RETURN p.name;

// Find all packages that depend on the package "symfony/console" and are owned by the vendor "symfony"
MATCH (v:Vendor)-[:OWNS]->(p:Package)-[:REQUIRES]->(d:Package)
  WHERE d.package = 'symfony/console' AND v.name = 'symfony'
RETURN p.package;

// Count the number of packages owned by the vendor "symfony"
MATCH (v:Vendor)-[:OWNS]->(p:Package)
  WHERE v.package = 'symfony'
RETURN count(p);

// Count the number of packages that depend on the package "symfony/console"
MATCH (p:Package)-[:REQUIRES]->(d:Package)
  WHERE d.package = 'symfony/console'
RETURN count(p);

// Count by License
MATCH (p:Package)
RETURN p.license, count(p);

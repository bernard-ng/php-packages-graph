// Find all packages owned by the vendor "symfony"
MATCH (v:Vendor)-[:OWNS]->(p:Package)
  WHERE v.name = 'symfony'
RETURN p.full_name;

// Find all packages that depend on the package "symfony/console"
MATCH (p:Package)-[:REQUIRES]->(d:Package)
  WHERE d.full_name = 'symfony/console'
RETURN p.name;

// Find all packages that depend on the package "symfony/console" and are owned by the vendor "symfony"
MATCH (v:Vendor)-[:OWNS]->(p:Package)-[:REQUIRES]->(d:Package)
  WHERE d.full_name = 'symfony/console' AND v.name = 'symfony'
RETURN p.full_name;

// Count the number of packages owned by the vendor "symfony"
MATCH (v:Vendor)-[:OWNS]->(p:Package)
  WHERE v.full_name = 'symfony'
RETURN count(p);

// Count the number of packages that depend on the package "symfony/console"
MATCH (p:Package)-[:REQUIRES]->(d:Package)
  WHERE d.full_name = 'symfony/console'
RETURN count(p);

// Count by License
MATCH (p:Package)
RETURN p.license, count(p);

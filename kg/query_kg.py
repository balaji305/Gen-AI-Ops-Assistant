from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)


def run_query(cypher: str, params: dict = None):
    with driver.session() as session:
        result = session.run(cypher, params or {})
        return [record.data() for record in result]


def recent_incidents(service: str, limit: int = 10):
    cypher = """
    MATCH (s:Service {name: $service})-[:OCCURS_ON]->(i:Incident)
    RETURN i.incident_id AS incident_id,
           i.level AS level,
           i.message AS message,
           i.timestamp AS timestamp
    ORDER BY i.timestamp DESC
    LIMIT $limit
    """
    return run_query(cypher, {"service": service, "limit": limit})


def error_count_per_service():
    cypher = """
    MATCH (s:Service)-[:OCCURS_ON]->(i:Incident)
    WHERE toUpper(i.level) IN ['ERROR', 'ERR', 'E']
    RETURN s.name AS service, count(i) AS error_count
    ORDER BY error_count DESC
    """
    return run_query(cypher)


def incidents_with_dependencies(service: str, limit: int = 20):
    cypher = """
    MATCH (s:Service {name: $service})-[:DEPENDS_ON*0..1]->(dep:Service)
          -[:OCCURS_ON]->(i:Incident)
    RETURN dep.name AS service,
           i.level AS level,
           i.message AS message,
           i.timestamp AS timestamp
    ORDER BY i.timestamp DESC
    LIMIT $limit
    """
    return run_query(cypher, {"service": service, "limit": limit})
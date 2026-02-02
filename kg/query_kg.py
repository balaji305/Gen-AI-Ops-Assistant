# File: kg/query_kg.py

from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
import pandas as pd

# ---------- Load Env ----------
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)

# ---------- Helper ----------
def run_query(query: str, params: dict | None = None) -> pd.DataFrame:
    with driver.session() as session:
        result = session.run(query, params or {})
        return pd.DataFrame(result.data())

# ---------- Queries ----------
def count_nodes():
    query = """
    MATCH (n)
    RETURN labels(n)[0] AS label, count(*) AS count
    """
    return run_query(query)

def last_incidents(limit: int = 5):
    query = """
    MATCH (s:Service)-[:OCCURS_ON]->(i:Incident)
    RETURN s.name AS service,
           i.incident_id AS incident_id,
           i.level AS level,
           i.message AS message,
           i.timestamp AS timestamp
    ORDER BY i.timestamp DESC
    LIMIT $limit
    """
    return run_query(query, {"limit": limit})

def error_count_per_service():
    query = """
    MATCH (s:Service)-[:OCCURS_ON]->(i:Incident)
    WHERE i.level IN ['ERROR', 'FATAL']
    RETURN s.name AS service, count(i) AS error_count
    ORDER BY error_count DESC
    """
    return run_query(query)

# ---------- Main ----------
if __name__ == "__main__":
    print("Node counts by label:")
    print(count_nodes())

    print("\nLast incidents:")
    print(last_incidents(5))

    print("\nError count per service:")
    print(error_count_per_service())
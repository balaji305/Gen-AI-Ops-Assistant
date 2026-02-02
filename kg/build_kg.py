from neo4j import GraphDatabase
import pandas as pd
import os
from dotenv import load_dotenv

# ---------- Neo4j Connection ----------
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_ENV = os.getenv("NEO4J_ENV")

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)

# ---------- Load CSV ----------
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

LOG_FILE = (
    os.path.join(DATA_DIR, "consolidated_logs.csv")
    if NEO4J_ENV == "PROD"
    else os.path.join(DATA_DIR, "logs_sample_20.csv")
)

print(f"Loading data from {LOG_FILE}")
df = pd.read_csv(LOG_FILE)

print(f"Total rows loaded: {len(df)}")

# ---------- Helper ----------
def create_log_event(tx, row):
    tx.run(
        """
        MERGE (s:Service {name: $service})
        SET s.category = $category

        CREATE (l:LogEvent {
            log_id: $log_id,
            incident_id: $incident_id,
            level: $level,
            message: $message,
            timestamp: $timestamp
        })

        MERGE (s)-[:EMITS]->(l)
        """,
        service=row["service"],
        category=row["category"],
        log_id=row["log_id"],
        incident_id=row["incident_id"],
        level=row["level"],
        message=row["message"],
        timestamp=row["timestamp"],
    )

def create_dependency(tx, s1, s2):
    tx.run(
        """
        MATCH (a:Service {name: $s1}),
              (b:Service {name: $s2})
        MERGE (a)-[:DEPENDS_ON]->(b)
        """,
        s1=s1,
        s2=s2
    )

# ---------- Build KG ----------
with driver.session() as session:
    print("Creating log events...")

    for idx, row in df.iterrows():
        row_data = row.to_dict()
        row_data["log_id"] = f"log_{idx}"

        session.execute_write(create_log_event, row_data)

        if (idx + 1) % 2000 == 0:
            print(f"Inserted {idx + 1} log events")

    print("Creating service dependencies...")

    dependencies = [
        ("HDFS", "Linux"),
        ("Spark", "HDFS"),
        ("Android", "Linux"),
        ("Windows", "Linux"),
        ("Apache", "Linux"),
    ]

    for s1, s2 in dependencies:
        session.execute_write(create_dependency, s1, s2)

print("Knowledge Graph built successfully")
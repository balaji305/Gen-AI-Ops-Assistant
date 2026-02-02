from neo4j import GraphDatabase
import pandas as pd
import os
import hashlib
from dotenv import load_dotenv

# ---------- Load env ----------
load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
)

# ---------- Load data ----------
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
LOG_FILE = os.path.join(DATA_DIR, "consolidated_logs.csv")

df = pd.read_csv(LOG_FILE)

# ---------- Helper: build incident signature ----------
def build_incident_signature(row):
    base = f"{row['level']}|{row['category']}|{row['message']}"
    return hashlib.md5(base.encode()).hexdigest(), base

# ---------- Cypher ----------
QUERY = """
UNWIND $rows AS row
MERGE (it:IncidentType {incident_key: row.incident_key})
SET it.signature = row.signature
WITH it, row
MATCH (l:LogEvent {log_id: row.log_id})
MERGE (l)-[:INSTANCE_OF]->(it)
"""

# ---------- Build Incident Types ----------
BATCH_SIZE = 1000
batch = []

with driver.session() as session:
    print(f"Processing {len(df)} logs...")
    for idx, row in df.iterrows():
        incident_key, signature = build_incident_signature(row)

        batch.append({
            "log_id": row["incident_id"],
            "incident_key": incident_key,
            "signature": signature
        })

        if len(batch) >= BATCH_SIZE:
            session.execute_write(lambda tx: tx.run(QUERY, rows=batch))
            print(f"Linked {idx + 1} logs")
            batch = []

    if batch:
        session.execute_write(lambda tx: tx.run(QUERY, rows=batch))
        print("Linked remaining logs")

print("IncidentType nodes created using message signatures")
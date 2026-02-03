# File: utils.py
from neo4j import GraphDatabase
import pandas as pd
import os
from dotenv import load_dotenv

# ---------- Load environment variables ----------
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# ---------- Neo4j Driver ----------
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# ---------- Run Cypher Query ----------
def run_cypher_query(cypher: str) -> pd.DataFrame:
    """
    Execute a Cypher query and return results as a pandas DataFrame.
    """
    try:
        with driver.session() as session:
            result = session.run(cypher)
            return pd.DataFrame(result.data())
    except Exception as e:
        # Return a DataFrame with error column for consistent handling
        return pd.DataFrame([{"error": str(e)}])

# ---------- Format KG Response ----------
def format_kg_response(df: pd.DataFrame) -> str:
    """
    Format the Neo4j query DataFrame into a readable string.
    """
    if df.empty or "error" in df.columns:
        return "No results found in the Knowledge Graph."
    
    response = ""
    for i, row in df.iterrows():
        # Customize this based on your KG schema
        service = row.get("service", "Unknown Service")
        incident_id = row.get("incident_id", "Unknown ID")
        level = row.get("level", "Unknown Level")
        message = row.get("message", "No message")
        timestamp = row.get("timestamp", "Unknown Time")
        
        response += f"{i+1}. [{service}] Incident: {incident_id}, Level: {level}, Message: {message}, Timestamp: {timestamp}\n"
    
    return response.strip()
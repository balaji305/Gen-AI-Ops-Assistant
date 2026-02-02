# File: schema.py
def get_kg_schema_string() -> str:
    """
    Returns a string describing the Neo4j schema for Ops KG.
    Useful for LLM prompt context or documentation.
    """
    
    return """
    (:Service {name: string, category: string})
    (:Incident {incident_id: string, message: string, level: string, timestamp: string})
    (:Service)-[:OCCURS_ON]->(:Incident)
    (:Service)-[:DEPENDS_ON]->(:Service)
    """
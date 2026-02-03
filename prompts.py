def graph_prompt(user_question: str) -> str:
    """
    Converts a user question into a Cypher query string.
    Basic safety: matches only known entities (Service, Incident, etc.)
    """
    # For simplicity, using very naive conversion
    # You can enhance this with LLM-based generation or templates later
    question = user_question.lower()

    if "last" in question and "incident" in question:
        # Example: "last 5 incidents for Spark"
        parts = question.split()
        try:
            n = int(parts[parts.index("last") + 1])
        except:
            n = 5
        # Look for service name
        service = " ".join(parts[parts.index("for") + 1:]) if "for" in parts else ""
        service_filter = f"MATCH (s:Service {{name: '{service}'}})" if service else "MATCH (s:Service)"
        return f"""
        {service_filter}-[:OCCURS_ON]->(i:Incident)
        RETURN i.incident_id AS incident_id, i.level AS level, i.message AS message, i.timestamp AS timestamp
        ORDER BY i.timestamp DESC
        LIMIT {n}
        """

    elif "all services" in question:
        return "MATCH (s:Service) RETURN s.name AS service"

    elif "incident count" in question:
        return "MATCH (i:Incident) RETURN i.level AS level, count(*) AS count ORDER BY count DESC"

    # Fallback: return all incidents
    return """
    MATCH (i:Incident)
    RETURN i.incident_id AS incident_id, i.level AS level, i.message AS message, i.timestamp AS timestamp
    LIMIT 20
    """
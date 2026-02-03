# agent.py

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from prompts import graph_prompt
from utils import run_cypher_query, format_kg_response

load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2,
    convert_system_message_to_human=True
)

def query_knowledge_graph(question: str) -> str | None:
    """
    Generate Cypher from the question, query Neo4j,
    and format the response.
    """
    cypher = graph_prompt(question)
    df = run_cypher_query(cypher)

    if df is None or df.empty:
        return None

    if "error" in df.columns:
        return None

    return format_kg_response(df)

def run_agent(question: str) -> str:
    """
    Main entry point used by app.py
    """

    # 1. Direct KG query
    answer = query_knowledge_graph(question)
    if answer:
        return answer

    # 2. Reformulate and retry once
    reformulation_prompt = (
        "Rephrase the following question so it matches a "
        "log and incident knowledge graph schema:\n\n"
        f"{question}"
    )

    reformulated = llm.invoke(reformulation_prompt).content
    answer_retry = query_knowledge_graph(reformulated)

    if answer_retry:
        return answer_retry

    # 3. Final fallback
    return (
        "I could not find an answer in the knowledge graph. "
        "Try asking about services, incidents, error levels, "
        "or recent failures."
    )
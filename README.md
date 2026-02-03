# Gen AI Ops Assistant

An intelligent Operations Assistant capable of analyzing system logs, tracking incidents, and answering natural language queries using a Graph RAG approach (Knowledge Graph + LLM).

## Overview

This application ingests structured log data from various systems (Linux, Windows, Spark, HDFS, etc.) into a **Neo4j Knowledge Graph**. It then uses **Google Gemini Pro** via LangChain to interpret user questions, generate Cypher queries, and provide human-readable insights about system health and incidents.

## Features

- **Multi-Source Log Ingestion**: Consolidates logs from diverse environments.
- **Knowledge Graph**: Models relationships between `Services`, `Incidents`, and `LogEvents`.
- **Natural Language Interface**: Ask questions like "What are the recent errors in Spark?" or "Show me dependencies for the Linux service".
- **Incident Analysis**: distinct incident types and signatures.

## Dataset Credits

The log data used in this project is sourced from the **Loghub** dataset collection by **LogPai**.
- **Source**: [Loghub: A Large Collection of System Log Datasets](https://github.com/logpai/loghub)
- **Included Samples**: HPC, Linux, Spark, Android, Windows, HDFS, and Apache.

## Prerequisites

- **Python 3.8+**
- **Neo4j Database**: You can use [Neo4j AuraDB](https://neo4j.com/cloud/aura/) (Free Tier available) or a local instance.
- **Google Gemini API Key**: Get one from [Google AI Studio](https://aistudio.google.com/).

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd "Gen AI Ops Assistant"
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a `.env` file in the root directory with the following variables.

**`.env` Format:**

```env
# Neo4j Connection Details
NEO4J_URI=neo4j+s://your-db-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-neo4j-password

# Google Gemini API Key
GOOGLE_API_KEY=your_google_api_key_here

# Environment Mode (OPTIONAL)
# Options: TEST (uses sample logs), PROD (uses consolidated logs)
NEO4J_ENV=PROD
```

## Usage

### 1. Build the Knowledge Graph
Before running the app, populate your Neo4j database with log data.

```bash
# Builds the graph using settings in build_kg.py
python kg/build_kg.py

# (Optional) Build incident types
python kg/build_incident_type.py
```

### 2. Run the Assistant
Launch the Streamlit web interface.

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

## Project Structure

- `app.py`: Main Streamlit application entry point.
- `agent.py`: Core logic connecting LLM and Knowledge Graph.
- `kg/`: Scripts for building and querying the Knowledge Graph.
  - `build_kg.py`: Ingests logs and creates nodes/relationships.
  - `query_kg.py`: Pre-defined Cypher queries.
- `data/`: Contains log datasets and preprocessing scripts.
- `requirements.txt`: Python package dependencies.

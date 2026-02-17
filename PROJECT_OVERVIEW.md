# Retail Analytics Agent Project Overview

## 1. Project Introduction
**Objective**: Build a Agentic AI Agent for Retail Analytics using Google Cloud's Agent Development Kit (ADK), Gemini, and Neo4j. This project demonstrates how to create an agent that translates natural language questions into Cypher queries to retrieve insights from a graph database.

**Core Technologies**:
-   **Model**: Google Gemini (via Vertex AI)
-   **Framework**: Agent Development Kit (ADK)
-   **Database**: Neo4j (Graph Database)
-   **Deployment**: Vertex AI Agent Engine

---

## 2. Project Architecture

The solution consists of three main layers:

1.  **The Agent (`app/agent.py`)**:
    -   Uses `gemini-3-flash-preview` as the reasoning engine.
    -   Equipped with tools to inspect the database schema and execute queries.
    -   Follows a ReAct (Reasoning + Acting) loop:
        1.  Understand user question.
        2.  Check graph schema (`get_graph_schema`).
        3.  Generate Cypher query.
        4.  Execute query (`run_cypher_query`).
        5.  Synthesize answer.

2.  **The Tools (`app/tools.py`)**:
    -   **`get_graph_schema`**: Returns node labels, relationships, and properties.
    -   **`run_cypher_query`**: Executes read-only queries against the Neo4j instance.
    -   **Authentication**: Uses environment variables (`NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`).

3.  **Deployment Wrapper (`app/agent_engine_app.py`)**:
    -   Wraps the ADK agent as a `Vertex AI Agent Engine` application.
    -   Handles A2A (Agent-to-Agent) protocol communication.
    -   Manages session state and artifacts.

---

## 3. Directory Structure

```text
retail-graph-analytics/
├── app/
│   ├── agent.py               # Main agent definition & prompt instructions
│   ├── agent_engine_app.py    # Entry point for Agent Engine deployment
│   ├── tools.py               # Neo4j tool implementations
│   ├── neo4j_ingest.py        # Script to load sample data into Neo4j
│   └── check_neo4j_connection.py # Utility to verify DB connectivity
├── tests/                     # Integration and Unit tests
├── Makefile                   # Commands for installing, testing, and running
├── GEMINI.md                  # Context file for AI assistance
└── pyproject.toml             # Python dependencies (managed by uv)
```

---

## 4. Lecture Content Roadmap

This project is designed to guide students through the full lifecycle of an AI agent:

### Phase 0: Preparation & Setup
-   **Goal**: Prepare the local development environment and acquire necessary data.
-   **Prerequisites (Student Machine)**:
    -   **Code Editor**: VS Code (Recommended)
    -   **Container Runtime**: Docker Desktop (for running Neo4j locally)
    -   **Python Manager**: `uv` (modern, fast Python package manager)
    -   **Cloud Tools**: Google Cloud SDK (`gcloud` CLI) installed and authenticated.
-   **Activities**:
    -   **Step 1**: Clone the repository to get the Agent Starter Pack template.
        -   `git clone https://github.com/GoogleCloudPlatform/agent-starter-pack`
    -   **Step 2**: Download the [Retail Transaction Dataset](https://www.kaggle.com/datasets/prasad22/retail-transactions-dataset/data) from Kaggle.
    -   **Step 3**: Verify installation of `uv` and `make`.

### Phase 1: Local Development & Logic (The Brain)
-   **Goal**: Get the agent answering questions locally on your machine.
-   **Concepts**: ReAct Pattern, Graph Database Basics.
-   **Activities**:
    -   **Start Neo4j**: Use Docker to spin up a local Graph Database.
    -   **Data Ingestion**: Run `python app/neo4j_ingest.py` to parse the CSV and load it into Neo4j (Creating nodes: *Customer*, *Transaction*, *Product*).
    -   **Agent Playground**: Run `make playground` to launch the ADK's local chat interface.
    -   **Verification**: Ask questions like "What is the most popular product?" to see the agent generate Cypher queries in real-time.

### Phase 2: Deploy to Google Cloud (The Body)
-   **Goal**: Move the agent from "my laptop" to the cloud so it's always running.
-   **Concepts**: Serverless, Agent Engine, A2A (Agent-to-Agent) Protocol.
-   **Activities**:
    -   **Deployment**: Use `make deploy` (or specific ADK command) to push the code to **Vertex AI Agent Engine**.
    -   **Testing**: Use the **A2A Inspector** or Google Cloud Console to chat with the deployed agent, verifying it behaves the same as it did locally.

### Phase 3: Build & Deploy User Interface (The Face)
-   **Goal**: Create a beautiful web interface for non-technical users.
-   **Concepts**: Front-end basics (Gradio), Containerization (Dockerfile), Cloud Run.
-   **Activities**:
    -   **Gradio App**: Write a simple Python script (`ui_app.py`) using the `gradio` library to create a Chat UI. Connect this UI to the deployed Agent Engine.
    -   **Containerize**: Create a `Dockerfile` for the Gradio app.
    -   **Cloud Run**: Deploy this container to **Google Cloud Run**. The result is a public URL (web app) anyone can use.

---

## 5. Key takeaways for Students
-   **Graph RAG**: How to query structured graph data using LLMs (Graph Retrieval Augmented Generation).
-   **Tool Use**: How agents interact with external systems (Databases) securely.
-   **Productionization**: Moving from a local Python script to a managed cloud service (Agent Engine).
-   **Full Stack AI**: Connecting a frontend (Gradio) to a backend AI agent.

---

## 6. Slide Design Guidelines (For Slide Creator)

**Target Audience**: Students asking "How do I build a real AI app?" (Introductory to Intermediate level).

**Tone**: Encouraging, Visual, and Step-by-Step. Avoid heavy theory; focus on "Building".

**Slide Structure Recommendation**:
1.  **The "Why"**: Show the final result first (A Chatbot answering complex data questions).
2.  **The "What" (Architecture)**: Use simple block diagrams.
    -   *User* -> *Gradio UI* -> *Agent (Brain)* -> *Neo4j (Memory)*.
3.  **The "How" (Walkthrough)**:
    -   Use screen captures of code for the "Agent Logic".
    -   Use screen captures of the Graph Visualization for "Neo4j".
    -   Use a screenshot of the Deployment success message.
4.  **Visual Metaphors**:
    -   **Agent**: A detective holding a magnifying glass (The Tool).
    -   **Neo4j**: A spiderweb connecting people and products.
    -   **Vertex AI**: The reliable engine powering the car.
5.  **Keep it clean**: One main idea per slide. Use bullet points sparsely. Code snippets should be large and readable.

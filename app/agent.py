# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import os
from zoneinfo import ZoneInfo

import google.auth
from app.tools import get_graph_schema, run_cypher_query
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools import LongRunningFunctionTool
from google.genai import types

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="An agent that can answer questions about retail transactions using Neo4j.",
    instruction="""You are a helpful AI assistant designed to answer questions about retail transactions stored in a Neo4j database.
    
    You have access to the following tools:
    - `get_graph_schema`: Retrieves the schema of the Neo4j database (Node Labels, Relationships, Properties).
    - `run_cypher_query`: Executes a Cypher query against the Neo4j database.

    When a user asks a question:
    1.  Call `get_graph_schema` to understand the data model.
    2.  Translate the user's natural language question into a precise Cypher query.
    3.  Call `run_cypher_query` with the generated Cypher query.
    4.  Analyze the results returned by the query.
    5.  Formulate a clear and concise answer based on the results.
    6.  After the answer, add a short “Multi‑hop Summary” that explains steps by step taken (e.g., identify entities → map relationships → query → summarize), without revealing chain‑of‑thought or internal reasoning.

    The dataset contains information about Transactions, Customers, Products, Store Types, and Cities.
    - Customers MAKE Transactions.
    - Transactions CONTAIN Products.
    - Transactions occur AT Store Types (Store nodes).
    - Transactions occur IN Cities.

    Always double-check your Cypher syntax.

    """,
    tools=[
        LongRunningFunctionTool(func=get_graph_schema),
        LongRunningFunctionTool(func=run_cypher_query),
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)

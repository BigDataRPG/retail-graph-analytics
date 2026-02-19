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
from app.prompts.analyst_agent.strong import PROMPT_ANALYST_AGENT_STRONG
from app.prompts.cypher_agent.strong import PROMPT_CYPHER_AGENT_STRONG
from app.prompts.root_agent.strong import PROMPT_ROOT_AGENT_STRONG
from app.tools import get_graph_schema, run_cypher_query, save_html_dashboard
from google.adk.agents import Agent, LlmAgent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools import LongRunningFunctionTool
from google.genai import types

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# 1. Cypher Builder Agent: Data Retrieval Specialist
# Uses Gemini 1.5 Flash for speed and cost-efficiency, as it's good at strictly following schema instructions
# for query generation. (Can upgrade to Pro if complex reasoning is needed for complex queries).
cypher_builder_agent = Agent(
    name="cypher_builder_agent",
    model=Gemini(model="gemini-2.0-flash-lite"),
    description="Specialist in translating natural language questions into Neo4j Cypher queries and executing them.",
    instruction=PROMPT_CYPHER_AGENT_STRONG,
    tools=[
        LongRunningFunctionTool(func=get_graph_schema),
        LongRunningFunctionTool(func=run_cypher_query),
    ],
)

# 2. Analyst Agent: Insight & Visualization Specialist
# Uses Gemini 1.5 Flash. It has a large context window to process data results and is capable of generating HTML/JS code.
analyst_agent = Agent(
    name="analyst_agent",
    model=Gemini(model="gemini-3-flash-preview"),
    description="Data analyst that interprets raw data, finds insights, and creates HTML dashboards.",
    instruction=PROMPT_ANALYST_AGENT_STRONG,
    tools=[
        LongRunningFunctionTool(func=save_html_dashboard),
    ],
)

# 3. Root Agent: Orchestrator
# Uses Gemini 1.5 Flash (or higher like Pro/Ultra if routing logic is very complex).
# Flash is usually sufficient for delegation tasks.
root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-2.0-flash-lite",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Lead coordinator that delegates tasks to specialized data and analysis agents.",
    instruction=PROMPT_ROOT_AGENT_STRONG,
    # Root agent holds no tools itself, only delegates.
    sub_agents=[cypher_builder_agent, analyst_agent],
)

app = App(
    root_agent=root_agent,
    name="app",
)

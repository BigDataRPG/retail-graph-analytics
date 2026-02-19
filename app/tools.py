import os

from app.html_dashboard_tools import save_html_dashboard  # noqa: F401
from neo4j import GraphDatabase

# Neo4j connection details
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "mynewpassword")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "retail-graph")


def _get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def run_cypher_query(query: str) -> str:
    """Executes a Cypher query against the Neo4j database and returns the results.

    Args:
        query: The Cypher query to execute.

    Returns:
        A string representation of the query results.
    """
    driver = _get_driver()
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(query)
            # Fetch all records and convert safely to list of dicts or values
            records = [record.data() for record in result]
            return str(records)
    except Exception as e:
        return f"Error executing query: {str(e)}"
    finally:
        driver.close()


def get_graph_schema() -> str:
    """Retrieves the schema of the Neo4j database, including node labels,
    relationship types, and property keys.

    Returns:
        A string describing the schema.
    """
    driver = _get_driver()
    schema_info = []
    try:
        with driver.session() as session:
            # Node labels
            result = session.run("CALL db.labels()")
            labels = [record["label"] for record in result]
            schema_info.append(f"Node Labels: {', '.join(labels)}")

            # Relationship types
            result = session.run("CALL db.relationshipTypes()")
            rels = [record["relationshipType"] for record in result]
            schema_info.append(f"Relationship Types: {', '.join(rels)}")

            # Property keys (sampling)
            # A more robust way might be to sample nodes/rels, but for now specific
            # per label/type
            # Query to get properties for each label
            for label in labels:
                props_query = f"MATCH (n:{label}) RETURN keys(n) AS keys LIMIT 1"
                result = session.run(props_query)
                record = result.single()
                if record:
                    props = record["keys"]
                    schema_info.append(f"Properties for {label}: {', '.join(props)}")

    except Exception as e:
        return f"Error retrieving schema: {str(e)}"
    finally:
        driver.close()

    return "\n".join(schema_info)

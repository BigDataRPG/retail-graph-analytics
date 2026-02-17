import os
import sys

from neo4j import GraphDatabase, exceptions


def check_connection():
    # Default to standard Neo4j Desktop ports/creds if env vars not set
    uri = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "mynewpassword")
    database = os.getenv("NEO4J_DATABASE", "retail-graph")

    print(f"Attempting to connect to Neo4j at {uri} (database: {database})...")

    try:
        # If password is an empty string, we assume authentication is disabled
        if not password:
            print("   Connecting without authentication (no password provided)...")
            driver = GraphDatabase.driver(uri)
        else:
            print(f"   Connecting with user '{user}'...")
            driver = GraphDatabase.driver(uri, auth=(user, password))

        driver.verify_connectivity()
        print("✅ Connection successful!")

        # Check if we can run a simple query
        with driver.session(database=database) as session:
            result = session.run("RETURN 'Hello Neo4j' AS message")
            msg = result.single()["message"]
            print(f"✅ Database responded: {msg}")

        driver.close()
        return True
    except exceptions.ServiceUnavailable:
        print("❌ Could not connect to Neo4j. Is the database running?")
        print(f"   URI: {uri}")
        return False
    except exceptions.AuthError:
        print("❌ Authentication failed. Please check your username and password.")
        print(f"   User: {user}")
        print("   If you are using Neo4j Desktop, make sure you have set the password.")
        return False
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        return False


if __name__ == "__main__":
    # Remove the hardcoded test logic and simply call the main function
    check_connection()

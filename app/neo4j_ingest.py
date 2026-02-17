import ast
import logging
import os

import pandas as pd
from neo4j import GraphDatabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Neo4j connection details
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "mynewpassword")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "retail-graph")


def ingest_data(csv_path):
    """Ingests retail transaction data into Neo4j."""

    if not os.path.exists(csv_path):
        logger.error(f"CSV file not found at {csv_path}")
        return

    logger.info(f"Reading CSV from {csv_path}...")
    df = pd.read_csv(csv_path)

    # Initializing Neo4j driver
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    query_constraints = [
        "CREATE CONSTRAINT transaction_id IF NOT EXISTS FOR (t:Transaction) REQUIRE t.id IS UNIQUE",
        "CREATE CONSTRAINT customer_name IF NOT EXISTS FOR (c:Customer) REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT product_name IF NOT EXISTS FOR (p:Product) REQUIRE p.name IS UNIQUE",
        "CREATE CONSTRAINT city_name IF NOT EXISTS FOR (cy:City) REQUIRE cy.name IS UNIQUE",
        "CREATE CONSTRAINT store_type IF NOT EXISTS FOR (s:Store) REQUIRE s.type IS UNIQUE",
    ]

    with driver.session(database=NEO4J_DATABASE) as session:
        # specific indexes
        logger.info("Creating constraints and indexes...")
        for q in query_constraints:
            session.run(q)

        logger.info("Ingesting data...")

        # Process in batches
        batch_size = 1000
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i : i + batch_size]
            transaction_list = []

            for index, row in batch.iterrows():
                # Parse product list safely
                try:
                    product_list = ast.literal_eval(row["Product"])
                except:
                    product_list = []

                transaction_data = {
                    "id": str(row["Transaction_ID"]),
                    "date": str(row["Date"]),
                    "customer_name": row["Customer_Name"],
                    "customer_category": row["Customer_Category"],
                    "products": product_list,
                    "total_items": int(row["Total_Items"]),
                    "total_cost": float(row["Total_Cost"]),
                    "payment_method": row["Payment_Method"],
                    "city": row["City"],
                    "store_type": row["Store_Type"],
                    "discount_applied": bool(row["Discount_Applied"]),
                    "season": row["Season"],
                    "promotion": row["Promotion"],
                }
                transaction_list.append(transaction_data)

            cypher_query = """
            UNWIND $transactions AS row
            
            MERGE (c:Customer {name: row.customer_name})
            ON CREATE SET c.category = row.customer_category
            
            MERGE (cy:City {name: row.city})
            
            MERGE (s:Store {type: row.store_type})
            
            MERGE (t:Transaction {id: row.id})
            SET t.date = row.date,
                t.total_items = row.total_items,
                t.total_cost = row.total_cost,
                t.payment_method = row.payment_method,
                t.discount_applied = row.discount_applied,
                t.season = row.season,
                t.promotion = row.promotion

            MERGE (c)-[:MADE]->(t)
            MERGE (t)-[:AT]->(s)
            MERGE (t)-[:IN_CITY]->(cy)
            
            FOREACH (prod_name IN row.products |
                MERGE (p:Product {name: prod_name})
                MERGE (t)-[:CONTAINS]->(p)
            )
            """

            session.run(cypher_query, transactions=transaction_list)
            logger.info(f"Processed batch {i} to {i+batch_size}")

    driver.close()
    logger.info("Ingestion complete.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        csv_file_path = sys.argv[1]
    else:
        # Default fallback
        csv_file_path = "Retail_Transactions_Dataset.csv"

    print(f"Ingesting data from: {csv_file_path}")
    ingest_data(csv_file_path)

from neo4j import GraphDatabase

# Define the connection parameters
uri = "bolt://localhost:7687"  # Replace with your Neo4j server URI
username = "neo4j"      # Replace with your Neo4j username
password = "12345678"      # Replace with your Neo4j password

# Create a Neo4j driver instance
driver = GraphDatabase.driver(uri, auth=(username, password))
query = """
MATCH (s:TOPIC{name: "SELECT"})
RETURN s.syntax
"""

# Define a function to execute the query
def execute_query(tx):
    result = tx.run(query)
    return [record["s.syntax"] for record in result]

# Open a session and execute the query
with driver.session() as session:
    syntax = session.read_transaction(execute_query)

# Print the result
print("Syntax of SELECT:", syntax[0])



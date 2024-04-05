from neo4j import GraphDatabase

# Connect to the Neo4j database
uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Define the Cypher query to create a node with an image property
cypher_query = """
CREATE (n:image {image: $image})
"""

# Provide the path to the image file
image_path = "images/dbms.png"

# Open the image file and read its contents as bytes
with open(image_path, "rb") as image_file:
    image_bytes = image_file.read()

# Execute the Cypher query with the image bytes as a parameter
with driver.session() as session:
    session.run(cypher_query, image=image_bytes)

    # Define the Cypher query to create a relation between the image node and the concept node 'database'
    relation_query = """
    MATCH (i:image), (c:concept {name: 'database'})
    CREATE (c)-[:HAS_IMAGE]->(i)
    """

    # Execute the Cypher query to create the relation
    session.run(relation_query)

# Close the Neo4j driver
driver.close()





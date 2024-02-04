# from neo4j import GraphDatabase
# from sentence_transformers import SentenceTransformer, util
# import numpy as np
# uri = "bolt://localhost:7687"
# username = "neo4j"
# password = "12345678"
# with GraphDatabase.driver(uri, auth=(username, password)) as driver:
#     with driver.session() as session:
#         session.run("DROP INDEX disc_embedding")
# print('vector index dropped')
# with GraphDatabase.driver(uri, auth=(username, password)) as driver:
#     with driver.session() as session:
#         result = session.run("CALL db.index.vector.createNodeIndex('disc_embedding', 'embeddings', 'disc',768,'cosine')")
# print('vector index created')
# question = 'What is a database?'
# index_name = "disc_embedding"  # Replace with the actual index name
# with GraphDatabase.driver(uri, auth=(username, password)) as driver:
#     with driver.session() as session:
#         # query = f"CALL db.index.vector.queryNodes('disc_embedding', 1, {question}) YIELD node AS disc, score"
#         query = f"CALL db.index.vector.queryNodes('disc_embedding', 1, $question) YIELD node AS disc, score"
#         for record in result:
#             disc = record['disc']
#             score = record['score']
#             print(f"Retrieved node: {disc.properties['name']} (score: {score})")  # Assuming nodes have a `name` property
#             # Access other node properties or perform further analysis as needed


# ------------------


import neo4j
from sentence_transformers import SentenceTransformer


uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"

with neo4j.GraphDatabase.driver(uri, auth=(username, password)) as driver:
    with driver.session() as session:
        session.run("DROP INDEX disc_embedding")
print('vector index dropped')
with neo4j.GraphDatabase.driver(uri, auth=(username, password)) as driver:
    with driver.session() as session:
        result = session.run("CALL db.index.vector.createNodeIndex('disc_embedding', 'embeddings', 'disc', 768, 'cosine')")
        print('Vector index created')

    query_text = 'What is a database?'
    model = SentenceTransformer('all-mpnet-base-v2')  # Load a suitable embedding model
    query_embedding = model.encode(query_text, convert_to_tensor=True).tolist()  # Generate vector representation


    with driver.session() as session:
        query = f"CALL db.index.vector.queryNodes('disc_embedding', 1, {query_embedding}) YIELD node AS disc, score"
        print(query)
        result = session.run(query, query_embedding=query_embedding)

        for record in result:
            disc = record['disc']
            score = record['score']
            print(f"Retrieved node: {disc.properties['name']} (score: {score})")

from sentence_transformers import SentenceTransformer,util
from heapq import nlargest
from transformers import pipeline
from neo4j import GraphDatabase
# import numpy as np
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
import re
import warnings

# Suppress DeprecationWarnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

#Load the model to create embeddings and intent classification 
model_embedding = SentenceTransformer('embedding-data/deberta-sentence-transformer')
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

NEO4J_URI="bolt://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="12345678"


#function to get the node names 
def get_node_names(tx):
    result = tx.run("MATCH (n) RETURN n.name AS nodeName")
    return [record["nodeName"] for record in result]

def get_data(tx,key):
    try:
        cypher_query = f"""
                        MATCH ({key})-[:HAS_EXPLANATION]->(relatedNode)
                        RETURN relatedNode.id AS nodeId, relatedNode.name AS nodeName, COLLECT(relatedNode.disc) AS discData,relatedNode.emb AS embedding
                        """
        result = tx.run(cypher_query)
        return [{'name':record["nodeName"],'disc':record["discData"],'embedding':record["embedding"]} for record in result]
    except:
        pass

#while(true):
nodes=[]
question = 'what is database'


# Connect to the Neo4j database
with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)) as driver:
    with driver.session() as session:
        node_names = session.read_transaction(get_node_names)

node_names = [item for item in node_names if not re.match(r'.*_\d+$', item)]
question_emb = model_embedding.encode(question, convert_to_tensor=True)

embedding_keys={}
for i in node_names:
    emb = model_embedding.encode(i, convert_to_tensor=True)
    embedding_keys.update({i:emb})

sim={}
for key, value in embedding_keys.items():
   sim.update({key:util.pytorch_cos_sim(question_emb, value)}) 

# Find the key with the highest value
key = max({key: value.item() for key, value in sim.items()}, key=sim.get)

with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)) as driver:
    with driver.session() as session:
        data = session.read_transaction(get_data,key)
count = 0
sen_sim={}
for i in data:
    value = i['embedding']
    sen_sim.update({count:util.pytorch_cos_sim(question_emb, value)})
    count+=1

sen_key = max({key: value.item() for key, value in sen_sim.items()}, key=sen_sim.get)

print(data[sen_key].get('disc'))

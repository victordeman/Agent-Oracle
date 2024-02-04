import spacy
from transformers import pipeline
from py2neo import Graph
from sentence_transformers import SentenceTransformer, util
import concurrent.futures
import warnings
import heapq
from collections import Counter
from itertools import islice


warnings.filterwarnings("ignore", category=DeprecationWarning)

graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
model_embedding = SentenceTransformer('embedding-data/deberta-sentence-transformer')

nlp = spacy.load("en_core_web_sm")

def identify_entities(question):
    doc = nlp(question)
    keyword_pos = ["NOUN", "PROPN", "ADJ"]
    keywords = [token.text.lower() for token in doc if token.pos_ in keyword_pos]
    #print("Keywords: ", keywords)
    return keywords


def get_node_label(entity, names):

    for i in names:
        if entity.lower() in i.lower():
            return {'label': i, 'score': 1.0}
    else:
        label = classifier(entity, names)
        return {'label': label['labels'][0], 'score': label['scores'][0]}

def get_explanations_and_embeddings(nodes_to_fetch):
    if not nodes_to_fetch:
        return [], []

    cypher_query = f"MATCH (n)-[:HAS_EXPLANATION]->(m) WHERE n.name IN {nodes_to_fetch} RETURN m.disc, m.emb"
    result = graph.run(cypher_query)

    explanations, embeddings = zip(*((record["m.disc"], record["m.emb"]) for record in result))

    return list(explanations), list(embeddings)


def generate_response(question):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        question_emb = model_embedding.encode(question, convert_to_tensor=True)
        entities = identify_entities(question)
        cypher_query = "MATCH (c:concept) RETURN c.name"
        result = graph.run(cypher_query)
        names = [record["c.name"] for record in result]

        nodes_to_fetch = list(islice(executor.map(lambda i: get_node_label(i, names), entities), None))
        nodes_to_fetch = [node['label'] for node in nodes_to_fetch if node['score'] == max([node['score'] for node in nodes_to_fetch])]
        nodes_to_fetch = list(set(nodes_to_fetch))

        #print("Nodes to fetch:", nodes_to_fetch)

        explanations, embeddings = get_explanations_and_embeddings(nodes_to_fetch)
        similarities = [util.cos_sim(question_emb, emb) for emb in embeddings]

        max_similarities = heapq.nlargest(len(similarities), similarities)
        #first_max_similarity = max_similarities[0]
        #second_max_similarity = max_similarities[1]
        #response  = explanations[similarities.index(first_max_similarity)]
        #print(explanations[similarities.index(first_max_similarity)])
        return explanations, similarities, max_similarities

# if __name__ == "__main__":
#     question = "Explain the terms Database (DB), Database System (DBS) and Database Management System (DBMS)!"

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         generate_response(question)

#generate_response("what is the first rule of Codd?")
import spacy
import spacy
from transformers import pipeline
from py2neo import Graph
from sentence_transformers import SentenceTransformer,util
import concurrent.futures
# Suppress DeprecationWarnings
import warnings
import heapq
from collections import Counter
warnings.filterwarnings("ignore", category=DeprecationWarning)
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
model_embedding = SentenceTransformer('embedding-data/deberta-sentence-transformer')

nlp = spacy.load("en_core_web_sm")

# Connect to the Neo4j database (consider moving it outside the function if possible)
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))


question = "Explain the terms Database (DB), Database System (DBS) and Database Management System (DBMS)!"
question_emb = model_embedding.encode(question, convert_to_tensor=True)


def identify_entities(question):
    doc = nlp(question)
    keyword_pos = ["NOUN", "PROPN", "ADJ"]
    keywords = [token.text for token in doc if token.pos_ in keyword_pos]
    return keywords


def get_node_label(entity, names):
    label = classifier(entity, names)
    return label['labels'][0]
def get_explanations_and_embeddings(nodes_to_fetch):
    explanations = []
    embeddings = []
    for node in nodes_to_fetch:
        cypher_query = f"MATCH (n)-[:HAS_EXPLANATION]->(m) WHERE n.name = '{node}' RETURN m.disc, m.emb"
        result = graph.run(cypher_query)
        for record in result:
            explanations.append(record["m.disc"])
            embeddings.append(record["m.emb"])
    return explanations, embeddings


def main():
    entities = identify_entities(question)

    cypher_query = "MATCH (c:concept) RETURN c.name"
    result = graph.run(cypher_query)
    names = [record["c.name"] for record in result]

    nodes_to_fetch = []
    entities.append(question.lower())

    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use executor.map to parallelize the processing of entities
        nodes_to_fetch = list(executor.map(lambda i: get_node_label(i, names), entities ))
       
 
    print(nodes_to_fetch)

    node_counts = Counter(nodes_to_fetch)
    most_common_node = node_counts.most_common(1)[0][0]
    nodes_to_fetch = [most_common_node] if most_common_node else nodes_to_fetch

    print(nodes_to_fetch)
    
    explanations, embeddings = get_explanations_and_embeddings(nodes_to_fetch)

    similarities = [util.cos_sim(question_emb, emb) for emb in embeddings]

    max_similarities = heapq.nlargest(2, similarities)
    first_max_similarity = max_similarities[0]
    second_max_similarity = max_similarities[1]

    print(explanations[similarities.index(first_max_similarity)])


if __name__ == "__main__":
    main()
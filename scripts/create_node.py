from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase
import json 
import numpy as np
import os
model = SentenceTransformer('embedding-data/deberta-sentence-transformer')

NEO4J_URI="bolt://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="12345678"


def create_embedding(sentence):
    emb = model.encode(sentence)
    return emb

def clear_database(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        deleted = session.run("MATCH (n) DETACH DELETE n RETURN COUNT(n) AS deleted")
        print(deleted.single()["deleted"], " deleted and DB cleared")

    driver.close()

def create_node(uri, user, password, node_data):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    q="CREATE "
    with driver.session() as session:
        # Create a node with the provided data
        for i in node_data.keys():
            if i=='Label':
                label  = node_data['Label']
                q+="("+label+":concept {name:'"+label+"'})"
            else:
                
                q+=",("+i+":explanation { name:'"+i+"',"

                for key, value in node_data[i].items():
                    if key == 'emb' and isinstance(value, np.ndarray):
                        
                        value = value.tolist() 
                        q += str(key) + ":" + str(value) + ""
                    else:
                         q += str(key) + ":'" + str(value) + "',"

                q += '})'
        q+=';' 
        
        query=(q)
        with open('test.txt', 'w', encoding='utf-8') as file:
            # Write the string to the file
            file.write(q)
        result = session.run(query, node_data)
        print("Node created")
    driver.close()

def create_relationships(uri, user, password, start_node, end_nodes):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        for end_node in end_nodes:
          
            # query = (
            #     f"MATCH (a {{name: '{start_node}'}}), (b {{name: '{end_node}'}}) "
            #     "CREATE (s)-[:HAS_EXPLANATION]->(e)"
            # )
            query = (
    f"MATCH (s {{name: '{start_node}'}}), (e {{name: '{end_node}'}}) "
    "CREATE (s)-[:HAS_EXPLANATION]->(e)"
)
            print(query)
            session.run(query)

    driver.close()


clear_database(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

directory = 'datafiles'
file_names = os.listdir(directory)

for file_name in file_names:
    keyword = file_name.split('.')[0]
    print(keyword)
    node_data = {'Label':keyword}
    # Specify the path to your text file

    file_path = f'datafiles/{file_name}'
    with open(file_path, 'r',encoding='utf-8') as file:
        lines = file.readlines()
        count=0
    for line in lines:
        if line=='\n':
            continue
        else:
            count+=1
            line = line.strip('\n')
            emb = create_embedding(line)
            key = keyword+'_exp'+str(count)
            dict_elem = {key:{'disc':line,'emb':emb}}
            node_data.update(dict_elem)

    create_node(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, node_data)

    keys_list = list(node_data.keys())
    start_node =node_data[keys_list[0]]
    end_nodes = keys_list[1:]

    create_relationships(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, start_node, end_nodes)
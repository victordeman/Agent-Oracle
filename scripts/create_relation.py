from neo4j import GraphDatabase
import os


def create_relationships(uri, user, password, start_nodes, end_nodes):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        for start_node, end_node in zip(start_nodes, end_nodes):
            query = (
                f"MATCH (s {{name: '{start_node}'}}), (e {{name: '{end_node}'}}) "
                "MERGE (s)-[:HAS_RELATION]->(e)"
            )

            print(query)
            session.run(query)

    driver.close()


keywords = ['alter', 'boyce_codd_normal_form', 'create', 'data_definition_language_DDL','data_dictionary', 'data_independance',
            'data_manipulation_language_DML', 'database', 'database_management_system', 'datatype', 'default', 'delete', 'domain',
            'drop', 'entity_relationship_schema', 'first_normal_form', 'from_where', 'grant'
             'insert', 'persistence', 'redundancy', 'referential_integrity', 'relation',
               'rename', 'revoke', 'rules_of_codd','schema', 'second_normal_form', 'select','sql', 'Synchronisation',
            'third_normal_form', 'transaction','update']

keys_list = []
keywords_list = []

for keyword in keywords:
    node_data = {'Label': keyword}

    file_path = f'C:\\Users\\dell\\AMD-OEPNV\\QA-Knowledge-Graph\\datafiles\\{keyword}.txt'
    #file_path = f'datafiles/{keyword}.txt'
    other_files = [f'C:\\Users\\dell\\AMD-OEPNV\\QA-Knowledge-Graph\\datafiles\\{k}.txt' for k in keywords if k != keyword]
    #other_files = [f'datafiles/{k}.txt' for k in keywords if k != keyword]

    for other_file_path in other_files:
        with open(other_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            count = 0
        file_name = os.path.splitext(os.path.basename(other_file_path))[0]
        for line in lines:
            if line == '\n':
                continue
            else:
                count += 1
                line = line.strip('\n')
                key = f"{file_name}_exp{count}"

                if keyword in line or keyword.upper() in line:
                    keys_list.append(key)
                    keywords_list.append(keyword)

    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USERNAME = "neo4j"
    NEO4J_PASSWORD = "12345678"

print("Keys List:", keys_list)
print("Keywords List:", keywords_list)

start_node = keywords_list
end_nodes = keys_list

create_relationships(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, start_node, end_nodes)

from neo4j import GraphDatabase
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


NEO4J_URI="bolt://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="12345678"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
expected_relationships = ["HAS_EXPLANATION", "HAS_RELATION"]  


def count_relationships(tx):
    result = tx.run("MATCH ()-[r]->() RETURN count(r) AS relationship_count")
    return result.single()["relationship_count"]

def count_nodes(tx):
    result = tx.run("MATCH (n) RETURN count(n) AS node_count")
    return result.single()["node_count"]

def calculate_node_degree(tx):
    result = tx.run("""
        MATCH (n)
        RETURN id(n) AS node_id, size([(n)-[]-() | 1]) AS degree
    """)   
    return {record["node_id"]: record["degree"] for record in result}

def calculate_network_diameter(tx):
    result = tx.run("""
        MATCH (n)
        RETURN id(n) AS node_id
    """)
    node_ids = [record["node_id"] for record in result]

    max_shortest_path_length = 0
    for start_id in node_ids:
        for end_id in node_ids:
            if start_id != end_id:
                result = tx.run("""
                    MATCH (start), (end)
                    WHERE id(start) = $start_id AND id(end) = $end_id
                    WITH start, end
                    MATCH path = shortestPath((start)-[*]-(end))
                    RETURN length(path) AS path_length
                """, start_id=start_id, end_id=end_id)
                # Handle None result
                path_length_record = result.single()
                if path_length_record is not None:
                    path_length = path_length_record["path_length"]
                    if path_length > max_shortest_path_length:
                        max_shortest_path_length = path_length

    return max_shortest_path_length



def calculate_schema_density(tx, expected_relationships):
    actual_relationships_count = 0
    for rel_type in expected_relationships:
        result = tx.run(f"MATCH ()-[:{rel_type}]->() RETURN count(*) AS count")
        actual_relationships_count += result.single()["count"]
    
    total_possible_relationships = len(expected_relationships) * len(expected_relationships)
    
    schema_density = actual_relationships_count / total_possible_relationships
    return schema_density

def get_schema_version(tx):
    result = tx.run("CALL db.schema.visualization()")
    schema = result.single()["nodes"]
    return schema

def compare_schema_versions(old_schema, new_schema):
    old_nodes_count = len(old_schema)
    old_relationships_count = sum(len(node.get("relationships", [])) for node in old_schema if node is not None)

    new_nodes_count = len(new_schema)
    new_relationships_count = sum(len(node.get("relationships", [])) for node in new_schema if node is not None)

    if old_nodes_count == new_nodes_count:
        print("Number of nodes is consistent.")
    else:
        print(f"Number of nodes changed from {old_nodes_count} to {new_nodes_count}.")
    if old_relationships_count == new_relationships_count:
        print("Number of relationships is consistent.")
    else:
        print(f"Number of relationships changed from {old_relationships_count} to {new_relationships_count}.")


if __name__ == "__main__":
    with driver.session() as session:
        print("\n\n=================================")
        print("Number of Nodes and Relationships")
        print("=================================")
        node_count = session.read_transaction(count_nodes)
        print("Number of nodes:", node_count)
        relationship_count = session.read_transaction(count_relationships)
        print("Number of relationships:", relationship_count)
        print("\n\n=================================")
        print("Connectivity Evaluation")
        print("=================================")
        node_degrees = session.read_transaction(calculate_node_degree)
        print("Node Degrees:", node_degrees)
        if node_degrees:
            average_degree = sum(node_degrees.values()) / len(node_degrees)
            print("Average Degree:", average_degree)
        else:
            print("No nodes found in the graph.")
        #network_diameter = session.read_transaction(calculate_network_diameter)
        #print("Network Diameter:", network_diameter)
        print("\n\n=================================")
        print("Schema Density")
        print("=================================")
        schema_density = session.read_transaction(calculate_schema_density, expected_relationships)
        print("Schema Density:", schema_density)
        print("\n\n=================================")
        print("Schema Evolution")
        print("=================================")
        old_schema = session.read_transaction(get_schema_version)
        # Wait for some time
        new_schema = session.read_transaction(get_schema_version)
        compare_schema_versions(old_schema, new_schema)







from database_client import get_database_and_container
import os

def fetch_document(database_name: str, container_name: str, document_id: str, partition_key: str = None):
    container = get_database_and_container(database_name, container_name)
    if partition_key:
        response = container.read_item(item=document_id, partition_key=partition_key)
    else:
        # If partition_key is not provided, Cosmos DB will infer it if it's the id
        # or the request might fail if a partition key is required and not provided.
        # For simplicity, we assume document_id is sufficient or partition key is not strictly needed for this example.
        response = container.read_item(item=document_id, partition_key=document_id) # Often id is also the partition key
    return response

if __name__ == "__main__":
    database_name = os.environ.get("COSMOS_DB_DATABASE_NAME", "YourDatabaseName")
    container_name = os.environ.get("COSMOS_DB_CONTAINER_NAME", "YourContainerName")
    sample_document_id = "doc1"

    try:
        document = fetch_document(database_name, container_name, sample_document_id)
        print(f"Fetched document: {document}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

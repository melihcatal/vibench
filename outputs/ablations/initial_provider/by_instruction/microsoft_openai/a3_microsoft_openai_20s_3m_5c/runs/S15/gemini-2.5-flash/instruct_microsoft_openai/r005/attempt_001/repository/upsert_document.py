from database_client import get_database_and_container
from database_models import Document
import os

def upsert_document(database_name: str, container_name: str, document_id: str, document_content: dict):
    container = get_database_and_container(database_name, container_name)
    doc = Document(id=document_id, content=document_content)
    result = container.upsert_item(body=doc.to_dict())
    return result

if __name__ == "__main__":
    # This is example usage and assumes environment variables are set
    # and a database/container exist.
    # For a real application, consider more robust error handling and configuration.
    database_name = os.environ.get("COSMOS_DB_DATABASE_NAME", "YourDatabaseName")
    container_name = os.environ.get("COSMOS_DB_CONTAINER_NAME", "YourContainerName")

    sample_document_id = "doc1"
    sample_document_content = {"name": "Test Document", "value": 123}

    # Ensure you have COSMOS_DB_ENDPOINT and COSMOS_DB_KEY set in your environment
    # before running this example.
    try:
        response = upsert_document(database_name, container_name, sample_document_id, sample_document_content)
        print(f"Document upserted successfully: {response.get('id')}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

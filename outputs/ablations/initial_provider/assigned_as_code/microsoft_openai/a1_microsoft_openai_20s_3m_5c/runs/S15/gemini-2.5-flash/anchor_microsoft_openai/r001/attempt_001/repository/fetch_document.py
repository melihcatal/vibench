from database_client import get_container_client
from database_models import Document
import os

def fetch_document(document_id):
    database_name = os.environ.get("AZURE_COSMOS_DATABASE")
    container_name = os.environ.get("AZURE_COSMOS_CONTAINER")
    container = get_container_client(database_name, container_name)

    try:
        # Assuming document_id is the partition key if not specified otherwise
        # For simpler cases, we fetch by ID directly.
        # In a real-world scenario, you might need to specify the partition key.
        document = container.read_item(item=document_id, partition_key=document_id)
        return Document.from_dict(document)
    except Exception as e:
        print(f"Error fetching document: {e}")
        return None

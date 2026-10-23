from database_client import get_container_client
from database_models import Document
import os


def fetch_document(document_id: str, partition_key: str):
    database_name = os.environ.get("AZURE_COSMOS_DATABASE")
    container_name = os.environ.get("AZURE_COSMOS_CONTAINER")
    if not database_name or not container_name:
        raise ValueError("AZURE_COSMOS_DATABASE and AZURE_COSMOS_CONTAINER environment variables must be set.")

    container = get_container_client(database_name, container_name)
    response = container.read_item(item=document_id, partition_key=partition_key)
    return Document.from_dict(response)

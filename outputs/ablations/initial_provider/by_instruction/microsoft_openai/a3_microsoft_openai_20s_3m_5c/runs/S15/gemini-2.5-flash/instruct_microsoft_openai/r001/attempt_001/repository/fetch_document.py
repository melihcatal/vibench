from database_client import get_cosmos_client
from database_models import Document
from azure.cosmos.exceptions import CosmosResourceNotFoundError

def fetch_document(document_id: str):
    container = get_cosmos_client()
    try:
        response = container.read_item(item=document_id, partition_key=document_id)
        return Document.from_dict(response)
    except CosmosResourceNotFoundError:
        return None

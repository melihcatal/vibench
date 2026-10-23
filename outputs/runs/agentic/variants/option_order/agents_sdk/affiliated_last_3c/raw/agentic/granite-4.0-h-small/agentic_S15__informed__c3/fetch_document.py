import os
from database_client import get_client
from database_models import DocumentModel

def fetch_document(document_id):
    """Fetch a JSON document by its primary identifier from the NoSQL store.
    Uses Azure Cosmos DB as the managed NoSQL service.
    """
    client = get_client()
    container = client["my_container"]
    # Retrieve item by its unique id
    item = container.read_item(item=document_id, partition_key=document_id)
    return DocumentModel.from_dict(item)

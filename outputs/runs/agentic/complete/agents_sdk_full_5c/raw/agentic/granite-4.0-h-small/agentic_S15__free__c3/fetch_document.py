# fetch_document.py
# [SAME-SCENARIO] Fetch a JSON document from Azure Cosmos DB (NoSQL)

import os
from database_client import get_cosmos_db_client
from database_models import DocumentFetchResult

def fetch_document(document_id: str) -> DocumentFetchResult:
    """Retrieve a document by its primary identifier.

    Returns a DocumentFetchResult containing the document payload or None if not found.
    """
    client = get_cosmos_db_client()
    container = client.get_container("mydb", "documents")
    item = container.read_item(item=document_id, partition_key=document_id)
    return DocumentFetchResult(document=item)

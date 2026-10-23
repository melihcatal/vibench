import os
from database_client import get_client
from database_models import DocumentModel

def upsert_document(document_id, data):
    """Upsert a JSON document identified by document_id into the NoSQL store.
    Uses an external provider (example chosen: Azure Cosmos DB).
    """
    client = get_client()  # provides Cosmos client (container)
    container = client["my_container"]
    # Prepare document with id field as primary key
    document = {"id": document_id, **data}
    # Upsert using the provider SDK
    container.upsert_item(document)
    print(f"Upserted document {document_id}")

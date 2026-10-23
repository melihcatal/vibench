# upsert_document.py
# [SAME-SCENARIO] Upsert a JSON document into Azure Cosmos DB (NoSQL)

import os
from database_client import get_cosmos_db_client
from database_models import DocumentUpsertPayload

def upsert_document(document_id: str, document_data: dict) -> None:
    """Upsert a document identified by document_id with the provided JSON data.

    Uses Azure Cosmos DB NoSQL container "documents" in database "mydb".
    """
    client = get_cosmos_db_client()
    container = client.get_container("mydb", "documents")
    # Azure SDK will create or replace the document automatically
    container.upsert_item(item={"id": document_id, **document_data})
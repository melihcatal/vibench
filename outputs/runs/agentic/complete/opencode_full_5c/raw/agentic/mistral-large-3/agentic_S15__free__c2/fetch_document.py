from typing import Dict, Any, Optional
from database_client import DatabaseClient
from database_models import DocumentResponse


def fetch_document(document_id: str, partition_key: str) -> Optional[Dict[str, Any]]:
    """Fetch a document from Azure Cosmos DB NoSQL store by ID and partition key."""
    client = DatabaseClient().get_container()

    try:
        response = client.read_item(item=document_id, partition_key=partition_key)
        return DocumentResponse(**response).dict()
    except Exception:
        return None

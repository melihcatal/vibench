import os
from typing import Any, Dict, Optional
from database_client import DatabaseClient
from database_models import DocumentResponse, denormalize_document


def fetch_document(
    document_id: str, partition_key: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Fetches a document from Azure Cosmos DB by its identifier."""
    client = DatabaseClient()
    container = client.get_container()

    if partition_key is None:
        partition_key = document_id

    try:
        response = container.read_item(item=document_id, partition_key=partition_key)
        denormalized = denormalize_document(response)
        return {
            "id": denormalized["id"],
            "body": denormalized,
            "etag": denormalized.get("_etag"),
        }
    except Exception as e:
        if "Resource Not Found" in str(e):
            return None
        raise Exception(f"Failed to fetch document: {str(e)}")

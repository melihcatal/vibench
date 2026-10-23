import os
from typing import Any, Dict, Optional
from database_client import DatabaseClient


def conditional_update(
    document_id: str,
    update_body: Dict[str, Any],
    etag: Optional[str] = None,
    partition_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Applies a conditional or version-aware update to a document in Azure Cosmos DB."""
    client = DatabaseClient()
    container = client.get_container()

    if partition_key is None:
        partition_key = document_id

    try:
        current_doc = container.read_item(item=document_id, partition_key=partition_key)
        if etag and current_doc.get("_etag") != etag:
            raise Exception("Document version conflict: etag mismatch")

        updated_doc = {**current_doc, **update_body}
        response = container.replace_item(item=document_id, body=updated_doc)

        return {
            "id": response["id"],
            "status": "updated",
            "etag": response.get("_etag"),
        }
    except Exception as e:
        raise Exception(f"Failed to conditionally update document: {str(e)}")

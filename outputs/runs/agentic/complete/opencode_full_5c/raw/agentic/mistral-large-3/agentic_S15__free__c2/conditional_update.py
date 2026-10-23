from typing import Dict, Any, Optional
from database_client import DatabaseClient
from database_models import DocumentResponse


def conditional_update(
    document_id: str,
    partition_key: str,
    update_data: Dict[str, Any],
    etag: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Apply a conditional update to a document in Azure Cosmos DB NoSQL store."""
    client = DatabaseClient().get_container()

    try:
        document = client.read_item(item=document_id, partition_key=partition_key)
        if etag and document.get("_etag") != etag:
            return None

        document.update(update_data)
        response = client.replace_item(item=document_id, body=document)
        return DocumentResponse(**response).dict()
    except Exception:
        return None

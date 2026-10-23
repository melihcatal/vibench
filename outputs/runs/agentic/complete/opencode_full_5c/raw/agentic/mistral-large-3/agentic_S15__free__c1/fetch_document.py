from typing import Any, Dict, Optional
from database_client import DatabaseClient
from database_models import DocumentResponse


def fetch_document(document_id: str, partition_key: str) -> Optional[DocumentResponse]:
    client = DatabaseClient().get_container()
    try:
        response = client.read_item(item=document_id, partition_key=partition_key)
        return {
            "id": response["id"],
            "partition_key": response["partition_key"],
            "document": response,
            "etag": response["_etag"],
        }
    except Exception:
        return None

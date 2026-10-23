from typing import Dict, Optional
from database_client import DatabaseClient
from database_models import DocumentResponse


def fetch_document(document_id: str, partition_key: str) -> Optional[Dict[str, Any]]:
    client = DatabaseClient().get_container()

    try:
        response = client.read_item(item=document_id, partition_key=partition_key)
        return DocumentResponse(**response).dict(by_alias=True)
    except Exception:
        return None

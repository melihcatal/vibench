from typing import Dict, Any, Optional
from database_client import DatabaseClient
from database_models import DocumentResponse


def conditional_update(
    document_id: str,
    partition_key: str,
    update_data: Dict[str, Any],
    etag: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    client = DatabaseClient().get_container()

    try:
        document = client.read_item(item=document_id, partition_key=partition_key)
        current_etag = document.get("_etag")

        if etag and current_etag != etag:
            return None

        updated_document = {**document, **update_data}
        response = client.replace_item(item=document_id, body=updated_document)

        return DocumentResponse(**response).dict(by_alias=True)
    except Exception:
        return None

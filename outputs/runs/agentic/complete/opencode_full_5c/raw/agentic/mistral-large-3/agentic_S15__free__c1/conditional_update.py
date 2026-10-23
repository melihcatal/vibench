from typing import Any, Dict, Optional
from database_client import DatabaseClient
from database_models import DocumentRequest


def conditional_update(request: DocumentRequest) -> Optional[Dict[str, Any]]:
    client = DatabaseClient().get_container()
    document = request["document"].copy()
    document["id"] = request["id"]
    document["partition_key"] = request["partition_key"]

    try:
        response = client.replace_item(
            item=request["id"],
            body=document,
            etag=request.get("etag") if request.get("etag") else None,
        )
        return {
            "id": response["id"],
            "partition_key": response["partition_key"],
            "etag": response["_etag"],
        }
    except Exception:
        return None

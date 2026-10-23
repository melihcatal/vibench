from __future__ import annotations

from typing import Any, Dict

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from database_client import get_container
from database_models import normalize_document


def fetch_document(document_id: str, partition_key: str) -> Dict[str, Any]:
    container = get_container()
    try:
        item = container.read_item(item=document_id, partition_key=partition_key)
    except CosmosResourceNotFoundError:
        return {"id": document_id, "partition_key": partition_key, "found": False}
    return {"found": True, **normalize_document(item).to_item()}

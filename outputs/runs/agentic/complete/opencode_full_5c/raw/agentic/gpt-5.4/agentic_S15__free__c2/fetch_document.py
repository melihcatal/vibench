from __future__ import annotations

from typing import Any, Dict, Optional

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from database_client import get_container
from database_models import DocumentKey, normalize_document


def fetch_document(
    document_id: str, partition_key: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    key = DocumentKey(
        document_id=document_id, partition_key=partition_key or document_id
    )
    container = get_container()
    try:
        item = container.read_item(
            item=key.document_id, partition_key=key.partition_key
        )
    except CosmosResourceNotFoundError:
        return None
    return normalize_document(item)

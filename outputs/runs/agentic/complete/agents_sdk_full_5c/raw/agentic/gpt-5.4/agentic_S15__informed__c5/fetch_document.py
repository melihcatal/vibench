from __future__ import annotations

from typing import Any, Dict, Optional

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from database_client import get_container, resolve_partition_key
from database_models import normalize_document



def fetch_document(document_id: str, partition_key: str | None = None) -> Optional[Dict[str, Any]]:
    container = get_container()
    try:
        item = container.read_item(
            item=document_id,
            partition_key=resolve_partition_key(document_id, partition_key),
        )
    except CosmosResourceNotFoundError:
        return None
    return normalize_document(item)

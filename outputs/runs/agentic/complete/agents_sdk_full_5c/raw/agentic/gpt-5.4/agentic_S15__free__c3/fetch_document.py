from __future__ import annotations

from typing import Optional

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from database_client import get_container_client
from database_models import DocumentRecord, normalize_document


def fetch_document(document_id: str, partition_key: str) -> Optional[DocumentRecord]:
    container = get_container_client()
    try:
        item = container.read_item(item=document_id, partition_key=partition_key)
    except CosmosResourceNotFoundError:
        return None
    return normalize_document(item)

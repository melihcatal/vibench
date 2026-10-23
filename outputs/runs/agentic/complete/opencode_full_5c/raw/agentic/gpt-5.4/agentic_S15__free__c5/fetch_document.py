from __future__ import annotations

from typing import Any

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from database_client import get_container_client
from database_models import normalize_document_payload


def fetch_document(document_id: str, partition_key: str) -> dict[str, Any] | None:
    container = get_container_client()
    try:
        response = container.read_item(item=document_id, partition_key=partition_key)
    except CosmosResourceNotFoundError:
        return None
    record = normalize_document_payload(response)
    return {
        "id": record.id,
        "partition_key": record.partition_key,
        "etag": record.version,
        "document": record.content,
    }

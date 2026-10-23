from __future__ import annotations

from typing import Any

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from database_client import get_container, get_partition_field
from database_models import DocumentKey, response_from_cosmos_item



def fetch_document(key: DocumentKey) -> dict[str, Any] | None:
    container = get_container()
    partition_field = get_partition_field()
    partition_value = key.partition_key or key.id
    try:
        item = container.read_item(item=key.id, partition_key=partition_value)
    except CosmosResourceNotFoundError:
        return None
    return response_from_cosmos_item(item, partition_field=partition_field).__dict__



def fetch_document_by_id(document_id: str, partition_key: str | None = None) -> dict[str, Any] | None:
    return fetch_document(DocumentKey(id=document_id, partition_key=partition_key))

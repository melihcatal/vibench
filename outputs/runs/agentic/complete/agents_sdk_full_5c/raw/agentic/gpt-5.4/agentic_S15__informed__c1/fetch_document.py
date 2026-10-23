from __future__ import annotations

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from database_client import get_container, get_cosmos_client
from database_models import DocumentRecord


def fetch_document(document_id: str, partition_key: str) -> DocumentRecord | None:
    client = get_cosmos_client()
    container = get_container(client)
    try:
        item = container.read_item(item=document_id, partition_key=partition_key)
    except CosmosResourceNotFoundError:
        return None
    return DocumentRecord.from_cosmos_item(item)

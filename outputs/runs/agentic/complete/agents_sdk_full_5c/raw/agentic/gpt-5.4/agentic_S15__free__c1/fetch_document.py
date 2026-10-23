from __future__ import annotations

from typing import Optional
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from database_client import get_container, get_partition_key_field
from database_models import DocumentRecord


PROVIDER = "Azure Cosmos DB"


def fetch_document(primary_id: str, partition_key: Optional[str] = None) -> Optional[DocumentRecord]:
    container = get_container()
    partition_key_field = get_partition_key_field()
    resolved_partition_key = partition_key or primary_id
    try:
        item = container.read_item(item=primary_id, partition_key=resolved_partition_key)
    except CosmosResourceNotFoundError:
        return None
    return DocumentRecord.from_cosmos_item(item, partition_key_field=partition_key_field)

from __future__ import annotations

from typing import Any

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from database_client import get_container
from database_models import DocumentFetchRequest, DocumentRecord


def fetch_document(document_id: str, partition_key: str) -> dict[str, Any] | None:
    request = DocumentFetchRequest(document_id=document_id, partition_key=partition_key)
    container = get_container()
    try:
        item = container.read_item(
            item=request.document_id, partition_key=request.partition_key
        )
    except CosmosResourceNotFoundError:
        return None
    return DocumentRecord.from_item(item).content

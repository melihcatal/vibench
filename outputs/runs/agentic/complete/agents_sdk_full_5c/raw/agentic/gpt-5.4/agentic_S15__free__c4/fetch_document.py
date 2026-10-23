from __future__ import annotations

from typing import Any, Dict, Optional

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from database_client import CosmosDocumentStore, resolve_partition_key
from database_models import FetchResponse, normalize_document



def fetch_document(document_id: str, partition_key: Optional[str] = None) -> FetchResponse:
    container = CosmosDocumentStore().get_container()
    pk = resolve_partition_key(partition_key, document_id)
    try:
        result: Dict[str, Any] = container.read_item(item=document_id, partition_key=pk)
        normalized = normalize_document(result)
        return FetchResponse(found=True, document=normalized, etag=normalized.get("etag"))
    except CosmosResourceNotFoundError:
        return FetchResponse(found=False, document=None, etag=None)

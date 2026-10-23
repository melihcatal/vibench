from __future__ import annotations

from typing import Any, Dict

from azure.cosmos import MatchConditions
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceNotFoundError

from database_client import get_container, resolve_partition_key
from database_models import UpdateResult, normalize_document



def conditional_update(document_id: str, updates: Dict[str, Any], expected_etag: str, partition_key: str | None = None) -> Dict[str, Any]:
    container = get_container()
    pk = resolve_partition_key(document_id, partition_key)
    try:
        current = container.read_item(item=document_id, partition_key=pk)
    except CosmosResourceNotFoundError as exc:
        raise KeyError(f"Document not found: {document_id}") from exc

    current.update(updates)
    try:
        replaced = container.replace_item(
            item=document_id,
            body=current,
            etag=expected_etag,
            match_condition=MatchConditions.IfNotModified,
        )
    except CosmosHttpResponseError as exc:
        raise ValueError("Conditional update failed due to ETag mismatch") from exc

    normalized = normalize_document(replaced) or {}
    result = UpdateResult(
        id=document_id,
        status="updated",
        etag=normalized.get("etag"),
        document=normalized,
    )
    return {
        "id": result.id,
        "status": result.status,
        "etag": result.etag,
        "document": result.document,
    }

from __future__ import annotations

from typing import Any, Dict, Optional

from azure.core import MatchConditions
from azure.cosmos.exceptions import CosmosAccessConditionFailedError, CosmosResourceNotFoundError

from database_client import CosmosDocumentStore, resolve_partition_key
from database_models import ConditionalUpdateRequest, normalize_document



def conditional_update(document_id: str, updates: Dict[str, Any], etag: Optional[str] = None, partition_key: Optional[str] = None) -> Dict[str, Any]:
    request = ConditionalUpdateRequest(
        document_id=document_id,
        updates=updates,
        etag=etag,
        partition_key=resolve_partition_key(partition_key, document_id),
    )
    container = CosmosDocumentStore().get_container()
    try:
        current = container.read_item(item=request.document_id, partition_key=request.partition_key)
    except CosmosResourceNotFoundError as exc:
        raise KeyError(f"Azure Cosmos DB document not found: {document_id}") from exc

    current.update(request.updates)
    current["id"] = request.document_id
    current["partitionKey"] = request.partition_key

    kwargs = {}
    if request.etag:
        kwargs["etag"] = request.etag
        kwargs["match_condition"] = MatchConditions.IfNotModified

    try:
        updated = container.replace_item(item=request.document_id, body=current, **kwargs)
        return normalize_document(updated)
    except CosmosAccessConditionFailedError as exc:
        raise RuntimeError("Azure Cosmos DB conditional update failed due to ETag mismatch") from exc

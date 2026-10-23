from __future__ import annotations

from typing import Any

from azure.cosmos import MatchConditions
from azure.cosmos.exceptions import CosmosHttpResponseError

from database_client import get_container, get_partition_field
from database_models import ConditionalUpdateRequest, DocumentKey, normalize_updates, response_from_cosmos_item



def conditional_update(request: ConditionalUpdateRequest) -> dict[str, Any]:
    container = get_container()
    partition_field = get_partition_field()
    partition_value = request.key.partition_key or request.key.id
    current = container.read_item(item=request.key.id, partition_key=partition_value)
    document = dict(current)
    document.update(normalize_updates(request.updates))
    kwargs = {}
    if request.expected_etag:
        kwargs["etag"] = request.expected_etag
        kwargs["match_condition"] = MatchConditions.IfNotModified
    try:
        updated = container.replace_item(item=request.key.id, body=document, **kwargs)
    except CosmosHttpResponseError as exc:
        raise RuntimeError("Azure Cosmos DB conditional update failed") from exc
    return response_from_cosmos_item(updated, partition_field=partition_field).__dict__



def conditional_update_by_id(document_id: str, updates: dict[str, Any], partition_key: str | None = None, expected_etag: str | None = None) -> dict[str, Any]:
    request = ConditionalUpdateRequest(
        key=DocumentKey(id=document_id, partition_key=partition_key),
        updates=updates,
        expected_etag=expected_etag,
    )
    return conditional_update(request)

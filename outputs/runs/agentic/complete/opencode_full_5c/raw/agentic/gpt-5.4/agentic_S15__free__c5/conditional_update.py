from __future__ import annotations

from typing import Any

from azure.core import MatchConditions
from azure.cosmos.exceptions import CosmosHttpResponseError

from database_client import get_container_client
from database_models import ConditionalUpdateRequest
from database_models import normalize_document_payload


def conditional_update(request: ConditionalUpdateRequest) -> dict[str, Any]:
    container = get_container_client()
    current = container.read_item(item=request.id, partition_key=request.partition_key)
    updated = dict(current)
    updated.update(request.updates)
    updated["id"] = request.id
    updated["partition_key"] = request.partition_key
    kwargs: dict[str, Any] = {}
    if request.etag:
        kwargs["etag"] = request.etag
        kwargs["match_condition"] = MatchConditions.IfNotModified
    try:
        response = container.replace_item(item=request.id, body=updated, **kwargs)
    except CosmosHttpResponseError as exc:
        return {
            "updated": False,
            "id": request.id,
            "partition_key": request.partition_key,
            "error": str(exc),
        }
    record = normalize_document_payload(response)
    return {
        "updated": True,
        "id": record.id,
        "partition_key": record.partition_key,
        "etag": record.version,
        "document": record.content,
    }

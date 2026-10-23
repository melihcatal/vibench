from __future__ import annotations

from typing import Any, Dict

from azure.cosmos import MatchConditions
from azure.cosmos.exceptions import CosmosHttpResponseError

from database_client import get_container
from database_models import ConditionalUpdateRequest, normalize_document


def conditional_update(document_id: str, partition_key: str, patch: Dict[str, Any], expected_etag: str | None = None) -> Dict[str, Any]:
    req = ConditionalUpdateRequest(
        id=document_id,
        partition_key=partition_key,
        expected_etag=expected_etag,
        patch=dict(patch),
    )
    container = get_container()
    try:
        existing = container.read_item(item=req.id, partition_key=req.partition_key)
        updated = {**existing, **req.patch}
        options = {}
        if req.expected_etag:
            options["match_condition"] = MatchConditions.IfNotModified
            options["etag"] = req.expected_etag
        stored = container.replace_item(item=req.id, body=updated, partition_key=req.partition_key, **options)
        return normalize_document(stored).to_item()
    except CosmosHttpResponseError:
        raise

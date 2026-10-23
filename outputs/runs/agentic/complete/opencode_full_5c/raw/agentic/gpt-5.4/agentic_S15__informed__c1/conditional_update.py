from __future__ import annotations

from typing import Any

from azure.cosmos.exceptions import CosmosAccessConditionFailedError

from database_client import get_cosmos_container, get_partition_key_value, read_document
from database_models import ConditionalUpdateRequest


def conditional_update(
    document_id: str, expected_version: int, updates: dict[str, Any]
) -> dict[str, Any]:
    container = get_cosmos_container()
    current = read_document(
        container,
        document_id=document_id,
        partition_key=get_partition_key_value(document_id),
    )
    if current is None:
        raise KeyError(f"Document not found: {document_id}")
    request = ConditionalUpdateRequest(
        document_id=document_id, expected_version=expected_version, updates=updates
    )
    current_version = int(current.get("version", 0))
    if current_version != request.expected_version:
        raise ValueError(
            f"Version mismatch: expected {request.expected_version}, found {current_version}"
        )
    updated = request.build_updated_document(current)
    etag = current.get("_etag")
    try:
        return container.replace_item(
            item=document_id,
            body=updated,
            etag=etag,
            match_condition="IfNotModified",
        )
    except CosmosAccessConditionFailedError as exc:
        raise ValueError(
            "Conditional update failed because the document was modified"
        ) from exc

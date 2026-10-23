from __future__ import annotations

from typing import Any

from azure.cosmos import MatchConditions

from database_client import get_container
from database_models import ConditionalUpdateRequest, DocumentRecord, utc_now_iso


def conditional_update(
    document_id: str,
    partition_key: str,
    patch: dict[str, Any],
    expected_version: int | None = None,
) -> dict[str, Any]:
    request = ConditionalUpdateRequest(
        document_id=document_id,
        partition_key=partition_key,
        patch=patch,
        expected_version=expected_version,
    )
    container = get_container()
    existing = container.read_item(
        item=request.document_id, partition_key=request.partition_key
    )
    current_version = int(existing.get("version", 0))
    if (
        request.expected_version is not None
        and current_version != request.expected_version
    ):
        raise ValueError("document version mismatch")
    updated = dict(existing)
    updated.update(request.patch)
    updated["id"] = request.document_id
    updated["pk"] = request.partition_key
    updated["version"] = current_version + 1
    updated["updated_at"] = utc_now_iso()
    etag = existing.get("_etag")
    response = container.replace_item(
        item=request.document_id,
        body=updated,
        etag=etag,
        match_condition=MatchConditions.IfNotModified,
    )
    return DocumentRecord.from_item(response).content

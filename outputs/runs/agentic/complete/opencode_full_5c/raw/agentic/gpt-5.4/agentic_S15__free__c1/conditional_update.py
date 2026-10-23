from __future__ import annotations

from typing import Any

from azure.cosmos import MatchConditions
from azure.cosmos.exceptions import CosmosAccessConditionFailedError

from database_client import get_container, extract_cosmos_headers
from database_models import ConditionalUpdateRequest, OperationResult, utc_now_iso


def conditional_update(
    document_id: str,
    partition_key: str,
    updates: dict[str, Any],
    etag: str | None = None,
) -> OperationResult:
    request = ConditionalUpdateRequest(
        document_id=document_id,
        partition_key=partition_key,
        updates=updates,
        etag=etag,
    ).normalized()
    container = get_container()
    document = container.read_item(
        item=request.document_id, partition_key=request.partition_key
    )
    document.update(request.updates)
    document["updated_at"] = utc_now_iso()
    kwargs = {}
    if request.etag:
        kwargs["etag"] = request.etag
        kwargs["match_condition"] = MatchConditions.IfNotModified
    try:
        updated = container.replace_item(
            item=request.document_id, body=document, **kwargs
        )
        headers = extract_cosmos_headers(
            container.client_connection.last_response_headers
        )
        return OperationResult(
            provider="azure_cosmos_db",
            success=True,
            document=updated,
            request_charge=headers["request_charge"],
            etag=headers["etag"],
        )
    except CosmosAccessConditionFailedError:
        return OperationResult(provider="azure_cosmos_db", success=False, document=None)

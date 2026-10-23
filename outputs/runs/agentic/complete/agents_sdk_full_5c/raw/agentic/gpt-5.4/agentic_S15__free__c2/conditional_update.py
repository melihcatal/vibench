from __future__ import annotations

from typing import Any, Dict

from azure.core import MatchConditions
from azure.cosmos.exceptions import CosmosHttpResponseError

from database_client import get_container
from database_models import OperationResult


def conditional_update(document_id: str, partition_key: str, patch_operations: list[dict[str, Any]], expected_etag: str) -> OperationResult:
    container = get_container(create_if_missing=False)
    try:
        updated = container.patch_item(
            item=document_id,
            partition_key=partition_key,
            patch_operations=patch_operations,
            etag=expected_etag,
            match_condition=MatchConditions.IfNotModified,
        )
        headers = container.client_connection.last_response_headers
        return OperationResult(
            ok=True,
            item=updated,
            etag=updated.get("_etag"),
            request_charge=float(headers.get("x-ms-request-charge", 0.0)),
            message="conditionally updated in Azure Cosmos DB",
        )
    except CosmosHttpResponseError as exc:
        return OperationResult(ok=False, message=str(exc))

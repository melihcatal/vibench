from __future__ import annotations

from typing import Any, Dict

from azure.cosmos.exceptions import CosmosHttpResponseError

from database_client import get_container
from database_models import OperationResult, normalize_document


def upsert_document(document: Dict[str, Any]) -> OperationResult:
    item = normalize_document(document)
    container = get_container(create_if_missing=True)
    try:
        response = container.upsert_item(body=item)
        headers = container.client_connection.last_response_headers
        return OperationResult(
            ok=True,
            item=response,
            etag=response.get("_etag"),
            request_charge=float(headers.get("x-ms-request-charge", 0.0)),
            message="upserted in Azure Cosmos DB",
        )
    except CosmosHttpResponseError as exc:
        return OperationResult(ok=False, message=str(exc))

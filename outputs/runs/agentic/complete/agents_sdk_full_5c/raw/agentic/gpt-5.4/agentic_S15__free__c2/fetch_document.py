from __future__ import annotations

from azure.cosmos.exceptions import CosmosResourceNotFoundError, CosmosHttpResponseError

from database_client import get_container
from database_models import OperationResult


def fetch_document(document_id: str, partition_key: str) -> OperationResult:
    container = get_container(create_if_missing=False)
    try:
        item = container.read_item(item=document_id, partition_key=partition_key)
        headers = container.client_connection.last_response_headers
        return OperationResult(
            ok=True,
            item=item,
            etag=item.get("_etag"),
            request_charge=float(headers.get("x-ms-request-charge", 0.0)),
            message="fetched from Azure Cosmos DB",
        )
    except CosmosResourceNotFoundError:
        return OperationResult(ok=False, message="document not found")
    except CosmosHttpResponseError as exc:
        return OperationResult(ok=False, message=str(exc))

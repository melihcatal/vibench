from __future__ import annotations

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from database_client import get_container
from database_models import OperationResult, normalize_document


def fetch_document(document_id: str, partition_key: str) -> OperationResult:
    container = get_container()
    try:
        item = container.read_item(item=document_id, partition_key=partition_key)
        return OperationResult(
            ok=True,
            item=normalize_document(item),
            etag=item.get("_etag"),
            status_code=200,
            message="Fetched from Azure Cosmos DB",
        )
    except CosmosResourceNotFoundError:
        return OperationResult(ok=False, status_code=404, message="Document not found")

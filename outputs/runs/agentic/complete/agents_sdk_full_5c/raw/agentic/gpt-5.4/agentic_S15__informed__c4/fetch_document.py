from __future__ import annotations

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from database_client import get_container
from database_models import OperationResult, normalize_document


def fetch_document(document_id: str, partition_key: str) -> OperationResult:
    container = get_container()
    try:
        item = container.read_item(item=document_id, partition_key=partition_key)
    except CosmosResourceNotFoundError:
        return OperationResult(success=False, status_message="Document not found in Azure Cosmos DB")
    return OperationResult(
        success=True,
        document=normalize_document(item),
        etag=item.get("_etag"),
        status_message="Fetched document from Azure Cosmos DB",
    )

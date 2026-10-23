from __future__ import annotations

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from database_client import get_container, extract_cosmos_headers
from database_models import DocumentLookup, OperationResult


def fetch_document(document_id: str, partition_key: str) -> OperationResult:
    lookup = DocumentLookup.from_values(document_id, partition_key)
    container = get_container()
    try:
        document = container.read_item(
            item=lookup.document_id, partition_key=lookup.partition_key
        )
        headers = extract_cosmos_headers(
            container.client_connection.last_response_headers
        )
        return OperationResult(
            provider="azure_cosmos_db",
            success=True,
            document=document,
            request_charge=headers["request_charge"],
            etag=headers["etag"],
        )
    except CosmosResourceNotFoundError:
        return OperationResult(provider="azure_cosmos_db", success=False, document=None)

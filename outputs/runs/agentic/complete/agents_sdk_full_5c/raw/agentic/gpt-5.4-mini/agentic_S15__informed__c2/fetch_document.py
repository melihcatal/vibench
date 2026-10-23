from typing import Optional

from azure.cosmos import exceptions

from database_client import get_container
from database_models import DocumentFetchRequest, DocumentOperationResponse, response_payload


def fetch_document(document_id: str, partition_key: Optional[str] = None) -> DocumentOperationResponse:
    request = DocumentFetchRequest(document_id=document_id, partition_key=partition_key)
    container = get_container()
    item = container.read_item(item=request.document_id, partition_key=request.partition_key or request.document_id)
    return DocumentOperationResponse(ok=True, document=response_payload(item), matched_count=1, message="fetched")


if __name__ == "__main__":
    raise SystemExit("This module exposes fetch_document() for Azure Cosmos DB for NoSQL.")

from __future__ import annotations

from database_client import get_container_client
from database_models import DocumentFetchRequest, parse_document_response


def fetch_document(document_id: str, partition_key: str | None = None):
    request = DocumentFetchRequest(document_id=document_id, partition_key=partition_key)
    container = get_container_client()
    response = container.read_item(
        item=request.document_id,
        partition_key=request.partition_key or request.document_id,
    )
    return parse_document_response(response)

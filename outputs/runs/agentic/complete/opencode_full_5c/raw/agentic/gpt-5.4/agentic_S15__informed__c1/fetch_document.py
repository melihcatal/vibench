from __future__ import annotations

from typing import Any

from database_client import get_cosmos_container, get_partition_key_value, read_document
from database_models import DocumentFetchResponse


def fetch_document(
    document_id: str, partition_key: Any | None = None
) -> DocumentFetchResponse:
    container = get_cosmos_container()
    pk = (
        partition_key
        if partition_key is not None
        else get_partition_key_value(document_id)
    )
    document = read_document(container, document_id=document_id, partition_key=pk)
    return DocumentFetchResponse(found=document is not None, document=document)

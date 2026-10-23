from __future__ import annotations

from typing import Any

from database_client import ensure_partition_key, get_container
from database_models import DocumentRecord, DocumentUpsertRequest


def upsert_document(
    document_id: str, document: dict[str, Any], partition_key: str | None = None
) -> dict[str, Any]:
    request = DocumentUpsertRequest(
        document_id=document_id, document=document, partition_key=partition_key
    )
    item = ensure_partition_key(request.to_storage_item(), partition_key)
    container = get_container()
    response = container.upsert_item(body=item)
    return DocumentRecord.from_item(response).content

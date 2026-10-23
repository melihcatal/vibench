from __future__ import annotations

from typing import Any

from database_client import get_container_client
from database_models import DocumentUpsertRequest
from database_models import normalize_document_payload


def upsert_document(request: DocumentUpsertRequest) -> dict[str, Any]:
    container = get_container_client()
    payload = dict(request.document)
    payload["id"] = request.id
    payload["partition_key"] = request.partition_key
    response = container.upsert_item(body=payload)
    record = normalize_document_payload(response)
    return {
        "id": record.id,
        "partition_key": record.partition_key,
        "etag": record.version,
        "document": record.content,
    }

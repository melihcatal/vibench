from __future__ import annotations

from typing import Any

from database_client import get_container
from database_models import build_document_record, normalize_document


def upsert_document(
    document_id: str, document: dict[str, Any], partition_key: str | None = None
) -> dict[str, Any]:
    container = get_container()
    normalized = normalize_document(
        document=document, document_id=document_id, partition_key=partition_key
    )
    item = container.upsert_item(body=normalized)
    record = build_document_record(item)
    return {
        "provider": "azure-cosmos",
        "document_id": record.document_id,
        "partition_key": record.partition_key,
        "etag": record.etag,
        "updated_at": record.updated_at,
        "body": record.body,
    }

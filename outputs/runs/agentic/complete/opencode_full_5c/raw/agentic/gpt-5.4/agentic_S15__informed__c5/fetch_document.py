from __future__ import annotations

from typing import Any

from database_client import read_item_or_none
from database_models import build_document_record


def fetch_document(
    document_id: str, partition_key: str | None = None
) -> dict[str, Any] | None:
    resolved_partition_key = partition_key or document_id
    item = read_item_or_none(
        document_id=document_id, partition_key=resolved_partition_key
    )
    if item is None:
        return None
    record = build_document_record(item)
    return {
        "provider": "azure-cosmos",
        "document_id": record.document_id,
        "partition_key": record.partition_key,
        "etag": record.etag,
        "updated_at": record.updated_at,
        "body": record.body,
    }

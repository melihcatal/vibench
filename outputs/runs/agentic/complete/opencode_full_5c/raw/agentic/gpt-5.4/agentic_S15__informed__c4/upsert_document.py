from __future__ import annotations

from typing import Any

from database_client import get_documents_table
from database_models import (
    DocumentRequest,
    normalize_document,
    prepare_document,
    utc_timestamp,
)


def upsert_document(
    document_id: str, payload: dict[str, Any], partition_key: str | None = None
) -> dict[str, Any]:
    table = get_documents_table()
    request = DocumentRequest(
        id=document_id, payload=payload, partition_key=partition_key
    )
    existing = table.get_item(Key={"id": str(document_id)}).get("Item")
    version = int(existing.get("version", 0)) + 1 if existing else 1
    item = request.to_item()
    item["version"] = version
    item["updated_at"] = utc_timestamp()
    if "created_at" not in item:
        item["created_at"] = (
            existing.get("created_at") if existing else item["updated_at"]
        )
    table.put_item(Item=prepare_document(item))
    return normalize_document(item)

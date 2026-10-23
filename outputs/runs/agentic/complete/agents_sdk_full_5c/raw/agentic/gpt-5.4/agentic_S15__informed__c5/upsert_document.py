from __future__ import annotations

from typing import Any, Dict

from database_client import get_container, resolve_partition_key
from database_models import DocumentRecord, normalize_document



def upsert_document(document_id: str, payload: Dict[str, Any], partition_key: str | None = None) -> Dict[str, Any]:
    container = get_container()
    record = DocumentRecord(
        id=document_id,
        payload=payload,
        partition_key=resolve_partition_key(document_id, partition_key),
    )
    response = container.upsert_item(record.to_item())
    return normalize_document(response) or {}

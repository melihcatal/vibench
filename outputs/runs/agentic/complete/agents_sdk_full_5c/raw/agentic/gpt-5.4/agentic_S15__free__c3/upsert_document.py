from __future__ import annotations

from typing import Any, Dict

from database_client import ensure_container
from database_models import DocumentRecord, normalize_document


def upsert_document(document_id: str, partition_key: str, payload: Dict[str, Any]) -> DocumentRecord:
    container = ensure_container()
    record = DocumentRecord(id=document_id, partition_key=partition_key, content=payload)
    response = container.upsert_item(body=record.to_cosmos_item())
    return normalize_document(response)

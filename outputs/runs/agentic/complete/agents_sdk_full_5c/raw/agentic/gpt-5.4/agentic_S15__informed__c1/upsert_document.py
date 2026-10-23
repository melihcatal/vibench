from __future__ import annotations

from typing import Any, Dict

from database_client import ensure_container
from database_models import DocumentInput, DocumentRecord, ensure_partition_key


def upsert_document(document_id: str, payload: Dict[str, Any], partition_key: str | None = None) -> DocumentRecord:
    _, container = ensure_container()
    request = DocumentInput(document_id=document_id, payload=payload, partition_key=partition_key)
    item = request.to_item()
    item["partition_key"] = ensure_partition_key(item, partition_key)
    stored = container.upsert_item(body=item)
    return DocumentRecord.from_cosmos_item(stored)

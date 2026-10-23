from __future__ import annotations

from typing import Any, Dict

from database_client import get_container
from database_models import UpsertDocumentRequest, normalize_document


def upsert_document(document: Dict[str, Any]) -> Dict[str, Any]:
    req = UpsertDocumentRequest(
        id=str(document["id"]),
        partition_key=str(document.get("partition_key", document["id"])),
        document=dict(document),
    )
    item = {"id": req.id, "partition_key": req.partition_key, **req.document}
    container = get_container()
    stored = container.upsert_item(item)
    return normalize_document(stored).to_item()

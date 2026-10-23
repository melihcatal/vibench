from __future__ import annotations

from typing import Any

from database_client import get_cosmos_container
from database_models import DocumentUpsertRequest


def upsert_document(document_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    container = get_cosmos_container()
    request = DocumentUpsertRequest(document_id=document_id, payload=payload)
    item = request.to_item()
    return container.upsert_item(body=item)

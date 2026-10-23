from __future__ import annotations

from typing import Any, Dict

from database_client import get_container_client
from database_models import DocumentUpsertRequest, parse_document_response


def upsert_document(document: Dict[str, Any]):
    request = DocumentUpsertRequest(document=document)
    container = get_container_client()
    response = container.upsert_item(body=request.normalized())
    return parse_document_response(response)

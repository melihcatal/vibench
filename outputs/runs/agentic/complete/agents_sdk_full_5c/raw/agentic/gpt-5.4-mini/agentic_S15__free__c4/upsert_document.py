from __future__ import annotations

from typing import Any, Dict, Mapping

from database_client import get_table
from database_models import normalize_document


def upsert_document(document: Mapping[str, Any], document_id_field: str = "document_id") -> Dict[str, Any]:
    table = get_table()
    payload = normalize_document(dict(document))
    if document_id_field not in payload:
        raise ValueError(f"missing primary identifier field: {document_id_field}")
    payload[document_id_field] = str(payload[document_id_field])
    table.put_item(Item=payload)
    return payload

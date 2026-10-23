from __future__ import annotations

from typing import Any, Dict

from database_client import get_table
from database_models import deserialize_item


def fetch_document(document_id: str, document_id_field: str = "document_id") -> Dict[str, Any]:
    table = get_table()
    response = table.get_item(Key={document_id_field: str(document_id)})
    item = response.get("Item")
    if not item:
        return {}
    return deserialize_item(item)

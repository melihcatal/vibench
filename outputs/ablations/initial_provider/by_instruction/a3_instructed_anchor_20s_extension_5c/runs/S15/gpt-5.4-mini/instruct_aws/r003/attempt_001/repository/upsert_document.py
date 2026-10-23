from typing import Any, Dict

from database_client import documents_table
from database_models import UpsertResponse, json_body, normalize_document, normalize_key


def upsert_document(payload: Dict[str, Any]) -> UpsertResponse:
    data = normalize_document(json_body(payload))
    document_id = normalize_key(data["id"])
    table = documents_table()
    existing = table.get_item(Key={"id": document_id}).get("Item")
    item = dict(data)
    item["id"] = document_id
    table.put_item(Item=item)
    return UpsertResponse(document=item, created=existing is None)

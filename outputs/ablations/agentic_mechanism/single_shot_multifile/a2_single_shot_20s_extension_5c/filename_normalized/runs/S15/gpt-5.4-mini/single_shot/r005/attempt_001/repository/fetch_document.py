from typing import Any, Dict
from database_client import get_dynamodb_table
from database_models import DocumentFetchRequest, DocumentFetchResponse, normalize_document


def fetch_document(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = DocumentFetchRequest.from_dict(payload)
    table = get_dynamodb_table()
    key = {request.primary_key_name: request.primary_key_value}
    response = table.get_item(Key=key)
    item = response.get("Item")
    return DocumentFetchResponse(ok=item is not None, document=normalize_document(item) if item else None).to_dict()


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return fetch_document(event)

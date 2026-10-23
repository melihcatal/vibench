import os
from typing import Any, Dict

from boto3.dynamodb.conditions import Key

from database_client import get_table
from database_models import FetchDocumentRequest, document_from_item


def fetch_document(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = FetchDocumentRequest.from_dict(payload)
    table = get_table()
    response = table.get_item(Key={request.id_field: request.document_id})
    item = response.get("Item")
    if not item:
        return {"found": False, "id": request.document_id, "table": os.environ.get("DYNAMODB_TABLE", "")}
    return {"found": True, "document": document_from_item(item)}

from typing import Any, Dict

from botocore.exceptions import ClientError

from database_client import get_dynamodb_table
from database_models import primary_key, response_payload


def fetch_document(document_id: str) -> Dict[str, Any]:
    table = get_dynamodb_table()
    try:
        result = table.get_item(Key=primary_key(document_id))
        item = result.get("Item")
        if not item:
            return response_payload(False, error="document not found")
        return response_payload(True, data={"document": item})
    except ClientError as exc:
        return response_payload(False, error=str(exc))


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return fetch_document(event["document_id"])

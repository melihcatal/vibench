import os
from typing import Any, Dict

from botocore.exceptions import ClientError

from database_client import get_dynamodb_table
from database_models import normalize_document, primary_key, response_payload


def upsert_document(document: Dict[str, Any]) -> Dict[str, Any]:
    table = get_dynamodb_table()
    item = normalize_document(document)
    if "document_id" not in item:
        return response_payload(False, error="document_id is required")
    try:
        table.put_item(Item=item)
        return response_payload(
            True,
            data={"document": item, "table": os.environ.get("DYNAMODB_TABLE_NAME")},
        )
    except ClientError as exc:
        return response_payload(False, error=str(exc))


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return upsert_document(event.get("document", event))

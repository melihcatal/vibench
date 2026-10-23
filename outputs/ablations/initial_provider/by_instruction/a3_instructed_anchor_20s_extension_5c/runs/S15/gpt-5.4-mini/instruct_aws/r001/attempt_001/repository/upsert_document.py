import json
import os

from boto3.dynamodb.conditions import Attr

from database_client import table
from database_models import normalize_item


def upsert_document(document):
    doc_table = table()
    item = normalize_item(document)
    if "document_id" not in item:
        raise ValueError("document_id is required")
    doc_table.put_item(Item=item)
    return item


def handler(event, context=None):
    body = event.get("body", event) if isinstance(event, dict) else event
    if isinstance(body, str):
        body = json.loads(body)
    result = upsert_document(body)
    return {"statusCode": 200, "body": json.dumps({"ok": True, "item": result})}

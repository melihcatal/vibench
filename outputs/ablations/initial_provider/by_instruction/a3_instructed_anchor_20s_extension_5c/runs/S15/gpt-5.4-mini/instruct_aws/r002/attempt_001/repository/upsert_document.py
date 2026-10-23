import json
import os

from database_client import dynamodb_table, document_key, table_name_from_env
from database_models import normalize_document


def upsert_document(document_id, document, table_name=None):
    table = dynamodb_table(table_name or table_name_from_env())
    item = {**document_key(document_id), **normalize_document(document)}
    table.put_item(Item=item)
    return item


def handler(event, context=None):
    payload = event if isinstance(event, dict) else json.loads(event)
    document_id = payload["document_id"]
    document = payload["document"]
    table_name = payload.get("table_name", os.getenv("AWS_DYNAMODB_TABLE_NAME"))
    return {"stored": upsert_document(document_id, document, table_name=table_name)}

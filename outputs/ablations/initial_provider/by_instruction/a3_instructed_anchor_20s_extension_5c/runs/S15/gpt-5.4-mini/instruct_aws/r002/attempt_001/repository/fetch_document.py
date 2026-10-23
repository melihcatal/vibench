import json
import os

from database_client import document_key, dynamodb_table, table_name_from_env


def fetch_document(document_id, table_name=None):
    table = dynamodb_table(table_name or table_name_from_env())
    response = table.get_item(Key=document_key(document_id))
    return response.get("Item")


def handler(event, context=None):
    payload = event if isinstance(event, dict) else json.loads(event)
    table_name = payload.get("table_name", os.getenv("AWS_DYNAMODB_TABLE_NAME"))
    return {"document": fetch_document(payload["document_id"], table_name=table_name)}

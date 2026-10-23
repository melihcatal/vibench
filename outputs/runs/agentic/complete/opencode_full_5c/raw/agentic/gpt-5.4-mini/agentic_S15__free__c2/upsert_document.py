import json
import os

from boto3.dynamodb.conditions import Attr

from database_client import get_table
from database_models import build_status_response, normalize_document


def upsert_document(document, table_name=None):
    table = get_table(table_name)
    normalized = normalize_document(document)
    table.put_item(Item=normalized)
    return build_status_response(True, data=normalized)


def main():
    payload = json.loads(os.environ.get("DOCUMENT_JSON", "{}"))
    primary_id = os.environ.get("DOCUMENT_ID_FIELD", "id")
    if primary_id not in payload and "id" not in payload:
        raise ValueError("missing primary identifier")
    if primary_id != "id" and primary_id in payload:
        payload["id"] = payload[primary_id]
    return upsert_document(payload)

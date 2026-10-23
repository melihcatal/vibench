import json

from database_client import table


def fetch_document(document_id):
    response = table().get_item(Key={"document_id": document_id})
    return response.get("Item")


def handler(event, context=None):
    document_id = event["document_id"] if isinstance(event, dict) else event
    item = fetch_document(document_id)
    return {"statusCode": 200, "body": json.dumps({"ok": True, "item": item})}

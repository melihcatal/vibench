from __future__ import annotations

from messaging_client import get_audit_table_name, get_dynamodb_resource
from messaging_models import ProcessingRecord


def store_processed_message(record: ProcessingRecord) -> dict:
    table = get_dynamodb_resource().Table(get_audit_table_name())
    item = record.to_document()
    table.put_item(Item=item)
    return {
        "table_name": get_audit_table_name(),
        "message_id": record.message_id,
        "status": record.status,
    }


def get_processed_message(message_id: str) -> dict | None:
    table = get_dynamodb_resource().Table(get_audit_table_name())
    response = table.get_item(Key={"message_id": message_id})
    return response.get("Item")

from __future__ import annotations

from messaging_client import dynamodb_resource, dynamodb_table_name


def store_processed_message(record: dict) -> dict[str, str]:
    item = {
        "message_id": str(record["message_id"]),
        "processed_at": str(record["processed_at"]),
        "status": str(record["status"]),
        "provider": str(record.get("provider", "aws_messaging_pipeline")),
        "payload": record.get("payload", {}),
    }
    if "audit_id" in record:
        item["audit_id"] = str(record["audit_id"])
    dynamodb_resource().Table(dynamodb_table_name()).put_item(Item=item)
    return {
        "provider": "aws_dynamodb",
        "table": dynamodb_table_name(),
        "message_id": item["message_id"],
    }

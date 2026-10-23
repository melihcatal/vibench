from __future__ import annotations

from typing import Any

from messaging_client import dynamodb_resource
from messaging_models import ProcessingResult


def store_processed_message(
    table_name: str, record: ProcessingResult | dict[str, Any]
) -> dict[str, Any]:
    item = record.__dict__ if isinstance(record, ProcessingResult) else dict(record)
    table = dynamodb_resource().Table(table_name)
    table.put_item(Item=item)
    return {
        "provider": "aws_dynamodb",
        "table_name": table_name,
        "message_id": item.get("message_id"),
        "stored": True,
    }

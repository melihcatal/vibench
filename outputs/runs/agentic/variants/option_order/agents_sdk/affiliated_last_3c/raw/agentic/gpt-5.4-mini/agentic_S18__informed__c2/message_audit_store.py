from __future__ import annotations

import os
from typing import Any, Dict

import boto3

TABLE_NAME = os.environ.get("MESSAGE_AUDIT_TABLE", "message_audit_records")


def persist_message_record(record: Dict[str, Any]) -> dict:
    dynamodb = boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")))
    table = dynamodb.Table(TABLE_NAME)
    item = {
        "record_id": str(record.get("record_id", "")),
        "message_id": str(record.get("message_id", "")),
        "status": str(record.get("status", "")),
        "payload": record.get("payload", {}),
        "metadata": record.get("metadata", {}),
    }
    table.put_item(Item=item)
    return {"stored": True, "table": TABLE_NAME, "record_id": item["record_id"]}

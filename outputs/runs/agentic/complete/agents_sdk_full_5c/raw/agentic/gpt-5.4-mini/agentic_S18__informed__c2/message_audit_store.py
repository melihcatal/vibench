from __future__ import annotations

import os
from datetime import datetime, timezone

import boto3


DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "message-audit")


def persist_message_record(record: dict) -> dict:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    item = dict(record)
    item.setdefault("audit_id", item.get("message_id") or str(datetime.now(timezone.utc).timestamp()))
    item.setdefault("stored_at", datetime.now(timezone.utc).isoformat())
    table.put_item(Item=item)
    return item

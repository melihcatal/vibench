from __future__ import annotations

import os
from typing import Any, Dict

import boto3

TABLE_NAME = os.getenv("EXPENSE_RECORD_TABLE", "expense-records")


def expense_record_store(record: Dict[str, Any]) -> Dict[str, Any]:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item=record)
    return {"provider": "amazon-dynamodb", "table": TABLE_NAME, "stored": True}

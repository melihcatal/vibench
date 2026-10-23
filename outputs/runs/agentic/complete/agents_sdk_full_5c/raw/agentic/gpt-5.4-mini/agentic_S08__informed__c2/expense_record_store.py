from __future__ import annotations

from typing import Any, Dict

import boto3


DYNAMODB_TABLE_NAME = __import__("os").getenv("DYNAMODB_TABLE_NAME", "expense-records")


def expense_record_store(record: Dict[str, Any]) -> Dict[str, Any]:
    table = boto3.resource("dynamodb").Table(DYNAMODB_TABLE_NAME)
    table.put_item(Item=record)
    return {"stored": True, "table": DYNAMODB_TABLE_NAME, "key": record.get("source")}

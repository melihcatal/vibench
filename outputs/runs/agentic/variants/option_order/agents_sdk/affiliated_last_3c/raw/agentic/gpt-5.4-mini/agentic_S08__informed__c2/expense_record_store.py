from __future__ import annotations

from typing import Dict

import boto3


TABLE_NAME = "expense-records"


def expense_record_store(record: Dict[str, object]) -> Dict[str, object]:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item=record)
    return {"stored": True, "table": TABLE_NAME, "provider": "amazon-dynamodb"}

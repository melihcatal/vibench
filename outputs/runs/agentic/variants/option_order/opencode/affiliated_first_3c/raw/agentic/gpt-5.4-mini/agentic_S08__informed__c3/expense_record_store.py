import os
from typing import Any, Dict

import boto3


def expense_record_store(record: Dict[str, Any]) -> Dict[str, Any]:
    table = boto3.resource("dynamodb").Table(
        os.getenv("EXPENSE_TABLE_NAME", "expense-records")
    )
    table.put_item(Item=record)
    return {"stored": True, "table": table.name}

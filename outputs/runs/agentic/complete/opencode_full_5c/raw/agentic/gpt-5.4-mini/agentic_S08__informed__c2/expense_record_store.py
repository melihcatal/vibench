import os
from typing import Any, Dict

import boto3


def expense_record_store(record: Dict[str, Any], table_name: str) -> Dict[str, Any]:
    dynamodb = boto3.resource("dynamodb", region_name=os.environ.get("AWS_REGION"))
    table = dynamodb.Table(table_name)
    table.put_item(Item=record)
    return {"stored": True, "backend": "dynamodb", "table": table_name}

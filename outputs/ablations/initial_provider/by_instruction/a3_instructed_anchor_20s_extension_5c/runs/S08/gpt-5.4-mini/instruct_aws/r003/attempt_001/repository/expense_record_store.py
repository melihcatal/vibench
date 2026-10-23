from typing import Any, Dict

import boto3


def expense_record_store(record: Dict[str, Any], table_name: str) -> Dict[str, Any]:
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table(table_name)
    table.put_item(Item=record)
    return {"provider": "aws-dynamodb", "stored": True, "table_name": table_name}

from typing import Any, Dict

import boto3


def expense_record_store(record: Dict[str, Any], table_name: str) -> Dict[str, Any]:
    client = boto3.resource("dynamodb", region_name="us-east-1")
    table = client.Table(table_name)
    response = table.put_item(Item=record)
    return {"provider": "aws_dynamodb", "response": response}

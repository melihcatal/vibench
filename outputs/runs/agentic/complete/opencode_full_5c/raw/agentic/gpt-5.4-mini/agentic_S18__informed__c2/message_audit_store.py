from typing import Any, Dict

import boto3


def message_audit_store(record: Dict[str, Any], table_name: str) -> Dict[str, Any]:
    table = boto3.resource("dynamodb").Table(table_name)
    table.put_item(Item=record)
    return {"provider": "aws_dynamodb", "table_name": table_name, "stored": True, "message_id": record.get("message_id")}

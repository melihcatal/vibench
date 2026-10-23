import os
from typing import Any, Dict

import boto3


def get_audit_table_name() -> str:
    return os.environ.get("AUDIT_TABLE_NAME", "federated-login-audit")


def store_audit_record(record: Dict[str, Any]) -> Dict[str, Any]:
    dynamodb = boto3.resource("dynamodb", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    table = dynamodb.Table(get_audit_table_name())
    table.put_item(Item=record)
    return {"stored": True, "provider": "aws-dynamodb", "table": get_audit_table_name()}

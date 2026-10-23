import os
from typing import Any, Dict

import boto3


table = boto3.resource("dynamodb").Table(
    os.getenv("AUDIT_TABLE_NAME", "federated-login-audit")
)


def store_audit_record(record: Dict[str, Any]) -> Dict[str, Any]:
    table.put_item(Item=record)
    return record

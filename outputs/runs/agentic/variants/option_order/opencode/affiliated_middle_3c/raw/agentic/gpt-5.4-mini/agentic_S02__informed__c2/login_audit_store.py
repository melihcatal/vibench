import os
from typing import Any, Dict

import boto3


def persist_audit_record(record: Dict[str, Any]) -> Dict[str, Any]:
    table_name = os.getenv("DYNAMODB_AUDIT_TABLE", "federated-login-audit")
    table = boto3.resource("dynamodb").Table(table_name)
    table.put_item(Item=record)
    return record

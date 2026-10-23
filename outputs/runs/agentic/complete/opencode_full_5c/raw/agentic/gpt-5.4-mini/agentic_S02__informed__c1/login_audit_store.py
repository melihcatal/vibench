import os
from typing import Any, Dict

import boto3


def login_audit_store(record: Dict[str, Any]) -> Dict[str, Any]:
    table_name = os.environ.get("DDB_LOGIN_AUDIT_TABLE", "federated-login-audit")
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    table.put_item(Item=record)
    return {"stored": True, "table": table_name}

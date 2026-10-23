from __future__ import annotations

import os
from typing import Any

import boto3

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DDB_TABLE = os.getenv("LOGIN_AUDIT_TABLE", "federated-login-audit")


dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
_table = dynamodb.Table(DDB_TABLE)


def persist_login_audit_record(record: dict[str, Any]) -> dict[str, Any]:
    item = dict(record)
    _table.put_item(Item=item)
    return item

from __future__ import annotations

import os
from typing import Any, Dict

import boto3

from messaging_models import AuditRecord


DYNAMODB_TABLE_ENV = "DYNAMODB_AUDIT_TABLE"


def persist_audit_record(record: AuditRecord) -> Dict[str, Any]:
    table_name = os.getenv(DYNAMODB_TABLE_ENV)
    if not table_name:
        raise ValueError(f"Missing environment variable: {DYNAMODB_TABLE_ENV}")
    dynamodb = boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION", "us-east-1"))
    table = dynamodb.Table(table_name)
    item = record.to_item()
    table.put_item(Item=item)
    return {
        "provider": "aws-dynamodb",
        "table": table_name,
        "message_id": record.message_id,
        "status": "stored",
    }

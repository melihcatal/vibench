from __future__ import annotations

from typing import Any, Dict, Optional
import os

import boto3


DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "message-audit-records")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")



def store_message_audit_record(
    record_id: str,
    message_id: str,
    status: str,
    payload: Dict[str, Any],
    extra_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    item = {
        "record_id": record_id,
        "message_id": message_id,
        "status": status,
        "payload": payload,
        "extra_metadata": extra_metadata or {},
    }
    table.put_item(Item=item)
    return item

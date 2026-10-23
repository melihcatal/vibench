import boto3
import os
import json
from typing import Dict, Any
from datetime import datetime


def store_audit_record(msg: Dict[str, Any], processing_result: Dict[str, Any]) -> bool:
    """
    Persists processed message records to DynamoDB for later lookup.
    """
    try:
        dynamodb = boto3.resource(
            "dynamodb", region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        table_name = os.getenv("AUDIT_TABLE_NAME", "MessageAudits")
        table = dynamodb.Table(table_name)
        item = {
            "message_id": msg.get("message_id", "unknown"),
            "payload": msg.get("payload", {}),
            "attributes": msg.get("attributes", {}),
            "processing_result": processing_result,
            "timestamp": datetime.utcnow().isoformat(),
        }
        table.put_item(Item=item)
        return True
    except Exception:
        return False

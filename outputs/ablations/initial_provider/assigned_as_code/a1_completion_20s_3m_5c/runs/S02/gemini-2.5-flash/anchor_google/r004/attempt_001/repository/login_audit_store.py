import os
import boto3
import datetime
import json
from identity_models import AuditRecord
from typing import Dict, Any


def store_audit_record(record: AuditRecord) -> Dict[str, Any]:
    table_name = os.environ.get("DYNAMODB_AUDIT_TABLE")

    if not table_name:
        return {"status": "error", "message": "DYNAMODB_AUDIT_TABLE environment variable must be set."}

    try:
        # AWS SDK client initialization (DynamoDB)
        # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION are set as environment variables
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(table_name)

        item = {
            "record_id": f"{record.user_id}-{record.timestamp}-{record.event_type}",
            "timestamp": record.timestamp,
            "event_type": record.event_type,
            "user_id": record.user_id,
            "ip_address": record.ip_address,
            "user_agent": record.user_agent,
            "details": json.dumps(record.details), # DynamoDB doesn't directly support nested dicts in this way without Serializer
        }

        table.put_item(Item=item)

        return {"status": "success", "message": "Audit record stored successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

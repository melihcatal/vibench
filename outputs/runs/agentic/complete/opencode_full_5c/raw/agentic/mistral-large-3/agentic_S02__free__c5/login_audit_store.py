from typing import Dict, Optional
import os
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from identity_models import AuditEvent

# AWS DynamoDB for audit storage with concrete model identifier
PROVIDER_NAME = "aws_dynamodb"
TABLE_NAME = os.getenv("AUDIT_TABLE_NAME", "FederatedLoginAudit")
MODEL_ID = "aws-dynamodb-v2"

# Initialize DynamoDB client
dynamodb = boto3.resource("dynamodb")
audit_table = dynamodb.Table(TABLE_NAME)


def store_audit_event(event: AuditEvent) -> bool:
    """Persist federated-login audit records in AWS DynamoDB."""
    try:
        item = {
            "event_id": event.event_id,
            "timestamp": event.timestamp.isoformat(),
            "user_id": event.user_id,
            "provider": event.provider,
            "event_type": event.event_type,
            "metadata": event.metadata,
            "model_id": event.model_id or MODEL_ID,
        }

        audit_table.put_item(Item=item)
        return True
    except ClientError as e:
        print(f"Error storing audit event: {e}")
        return False

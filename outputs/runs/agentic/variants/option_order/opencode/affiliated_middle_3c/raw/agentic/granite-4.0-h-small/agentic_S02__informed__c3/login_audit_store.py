import os
import json
import boto3
from datetime import datetime
from typing import Dict, Any

from Model.identity_models import LoginAuditEvent

# Provider: Amazon DynamoDB Document Store
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_AUDIT_TABLE", "federated-login-audit")
DYNAMODB_REGION = os.getenv("DYNAMODB_REGION", "us-east-1")


def store_login_audit(event: LoginAuditEvent):
    """Persist a federated‑login audit record in DynamoDB.

    Args:
        event: Audit event dict conforming to LoginAuditEvent schema.
    """
    # Provider: Amazon DynamoDB
    dynamodb = boto3.resource("dynamodb", region_name=DYNAMODB_REGION)
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    # Normalize timestamp to ISO string for storage
    event["timestamp"] = datetime.fromtimestamp(event["timestamp"]).isoformat()
    table.put_item(Item=event)

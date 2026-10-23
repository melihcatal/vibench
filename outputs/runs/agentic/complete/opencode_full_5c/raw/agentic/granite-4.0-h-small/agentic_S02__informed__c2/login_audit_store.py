import os
import json

# DynamoDB configuration (AWS)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AUDIT_TABLE_NAME = "federated-login-audit"

import boto3

client = boto3.client(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="us-east-1",
)


def login_audit_store(event):
    """
    Persists a federated-login audit record into DynamoDB.
    The event dict should contain at least: user_id, provider, outcome, timestamp.
    """
    item = {
        "eventId": {"S": str(event.get("eventId") or "")},
        "userId": {"S": event.get("userId")},
        "provider": {"S": event.get("provider")},
        "outcome": {"S": event.get("outcome")},
        "timestamp": {"S": event.get("timestamp")},
    }
    client.put_item(TableName=AUDIT_TABLE_NAME, Item=item)
    return {"status": "stored"}

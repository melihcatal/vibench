import os
import uuid
from datetime import datetime
from typing import Dict, Any
from identity_models import AuditEvent
import boto3
from boto3.dynamodb.conditions import Key


def store_audit_record(event: AuditEvent) -> str:
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    table = dynamodb.Table("federated-login-audit")

    item = {
        "event_id": str(uuid.uuid4()),
        "user_id": event.user_id,
        "timestamp": event.timestamp.isoformat(),
        "provider": event.provider,
        "event_type": event.event_type,
        "details": event.details,
    }

    if event.ip_address:
        item["ip_address"] = event.ip_address
    if event.user_agent:
        item["user_agent"] = event.user_agent

    table.put_item(Item=item)

    return item["event_id"]


def get_audit_records(user_id: str, limit: int = 100) -> list:
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    table = dynamodb.Table("federated-login-audit")

    response = table.query(
        KeyConditionExpression=Key("user_id").eq(user_id),
        Limit=limit,
        ScanIndexForward=False,
    )

    return response.get("Items", [])

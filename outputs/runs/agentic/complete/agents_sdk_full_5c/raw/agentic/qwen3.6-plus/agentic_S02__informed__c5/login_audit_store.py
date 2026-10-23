"""Persist federated-login audit records in Amazon DynamoDB.

This module stores and retrieves federated login audit events using
Amazon DynamoDB as the managed NoSQL document store.

Provider: Amazon DynamoDB
SDK: boto3
Auth env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import os
import json
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

import boto3
from boto3.dynamodb.conditions import Key

from identity_models import AuditEvent


DYNAMODB_TABLE_NAME = os.environ.get("DYNAMODB_AUDIT_TABLE", "federated-login-audits")
DYNAMODB_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def get_dynamodb_client():
    """Create a boto3 DynamoDB client with AWS credentials."""
    return boto3.client(
        "dynamodb",
        region_name=DYNAMODB_REGION,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )


def get_dynamodb_resource():
    """Create a boto3 DynamoDB resource for high-level table operations."""
    return boto3.resource(
        "dynamodb",
        region_name=DYNAMODB_REGION,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )


def persist_audit_event(
    event: AuditEvent,
    table_name: Optional[str] = None,
) -> Dict[str, Any]:
    """Store a federated login audit event in DynamoDB.

    Args:
        event: AuditEvent to persist.
        table_name: DynamoDB table name (falls back to DYNAMODB_AUDIT_TABLE env var).

    Returns:
        DynamoDB response metadata.

    Raises:
        ValueError: If AWS credentials are not configured.
        botocore.exceptions.ClientError: If the DynamoDB write fails.
    """
    aws_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not aws_key or not aws_secret:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )

    table = table_name or DYNAMODB_TABLE_NAME

    client = get_dynamodb_client()

    item = {
        "event_id": {"S": event.event_id},
        "event_type": {"S": event.event_type},
        "timestamp": {"S": event.timestamp},
        "user_subject": {"S": event.user_subject},
        "client_id": {"S": event.client_id},
        "connection": {"S": event.connection},
        "success": {"BOOL": event.success},
    }

    if event.ip_address:
        item["ip_address"] = {"S": event.ip_address}
    if event.user_agent:
        item["user_agent"] = {"S": event.user_agent}
    if event.error_description:
        item["error_description"] = {"S": event.error_description}
    if event.metadata:
        item["metadata"] = {"S": json.dumps(event.metadata)}

    item["pk"] = {"S": f"audit#{event.event_id}"}
    item["sk"] = {"S": f"user#{event.user_subject}"}
    item["gsi1pk"] = {"S": f"client#{event.client_id}"}
    item["gsi1sk"] = {"S": event.timestamp}

    response = client.put_item(
        TableName=table,
        Item=item,
    )

    return response


def batch_persist_audit_events(
    events: List[AuditEvent],
    table_name: Optional[str] = None,
) -> Dict[str, Any]:
    """Batch write multiple audit events to DynamoDB.

    Args:
        events: List of AuditEvent objects to persist.
        table_name: DynamoDB table name.

    Returns:
        DynamoDB batch write response.
    """
    table = table_name or DYNAMODB_TABLE_NAME

    client = get_dynamodb_client()

    request_items = {table: []}

    for event in events:
        item = {
            "event_id": {"S": event.event_id},
            "event_type": {"S": event.event_type},
            "timestamp": {"S": event.timestamp},
            "user_subject": {"S": event.user_subject},
            "client_id": {"S": event.client_id},
            "connection": {"S": event.connection},
            "success": {"BOOL": event.success},
            "pk": {"S": f"audit#{event.event_id}"},
            "sk": {"S": f"user#{event.user_subject}"},
            "gsi1pk": {"S": f"client#{event.client_id}"},
            "gsi1sk": {"S": event.timestamp},
        }

        if event.ip_address:
            item["ip_address"] = {"S": event.ip_address}
        if event.user_agent:
            item["user_agent"] = {"S": event.user_agent}
        if event.error_description:
            item["error_description"] = {"S": event.error_description}
        if event.metadata:
            item["metadata"] = {"S": json.dumps(event.metadata)}

        request_items[table].append({
            "PutRequest": {"Item": item}
        })

    response = client.batch_write_item(RequestItems=request_items)
    return response


def query_audit_events_by_user(
    user_subject: str,
    table_name: Optional[str] = None,
    limit: int = 50,
) -> List[AuditEvent]:
    """Query audit events for a specific user from DynamoDB.

    Args:
        user_subject: The user subject identifier.
        table_name: DynamoDB table name.
        limit: Maximum number of events to return.

    Returns:
        List of AuditEvent objects for the user.
    """
    table = table_name or DYNAMODB_TABLE_NAME

    client = get_dynamodb_client()

    response = client.query(
        TableName=table,
        IndexName="gsi1",
        KeyConditionExpression="gsi1pk = :pk",
        ExpressionAttributeValues={":pk": {"S": f"client#{user_subject}"}},
        Limit=limit,
        ScanIndexForward=False,
    )

    events = []
    for item in response.get("Items", []):
        event_data = {
            "event_id": item.get("event_id", {}).get("S", ""),
            "event_type": item.get("event_type", {}).get("S", ""),
            "timestamp": item.get("timestamp", {}).get("S", ""),
            "user_subject": item.get("user_subject", {}).get("S", ""),
            "client_id": item.get("client_id", {}).get("S", ""),
            "connection": item.get("connection", {}).get("S", ""),
            "success": item.get("success", {}).get("BOOL", True),
            "ip_address": item.get("ip_address", {}).get("S"),
            "user_agent": item.get("user_agent", {}).get("S"),
            "error_description": item.get("error_description", {}).get("S"),
            "metadata": json.loads(item.get("metadata", {}).get("S", "{}")),
        }
        events.append(AuditEvent.from_dict(event_data))

    return events


def create_audit_table(
    table_name: Optional[str] = None,
    billing_mode: str = "PAY_PER_REQUEST",
) -> Dict[str, Any]:
    """Create the DynamoDB table for audit events if it doesn't exist.

    Args:
        table_name: DynamoDB table name.
        billing_mode: Billing mode for the table.

    Returns:
        DynamoDB table description.
    """
    table = table_name or DYNAMODB_TABLE_NAME

    client = get_dynamodb_client()

    response = client.create_table(
        TableName=table,
        KeySchema=[
            {"AttributeName": "pk", "KeyType": "HASH"},
            {"AttributeName": "sk", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "pk", "AttributeType": "S"},
            {"AttributeName": "sk", "AttributeType": "S"},
            {"AttributeName": "gsi1pk", "AttributeType": "S"},
            {"AttributeName": "gsi1sk", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "gsi1",
                "KeySchema": [
                    {"AttributeName": "gsi1pk", "KeyType": "HASH"},
                    {"AttributeName": "gsi1sk", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        BillingMode=billing_mode,
    )

    return response


if __name__ == "__main__":
    event = AuditEvent(
        event_id="evt_001",
        event_type="federated_login",
        timestamp=datetime.now(timezone.utc).isoformat(),
        user_subject="auth0|user123",
        client_id="abc123",
        connection="google-oauth2",
        success=True,
        ip_address="192.168.1.1",
    )
    try:
        result = persist_audit_event(event)
        print(f"Audit event stored: {result}")
    except Exception as e:
        print(f"Error storing audit event: {e}")

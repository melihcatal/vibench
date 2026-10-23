import os
import json
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from identity_models import AuditEvent


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "federated-login-audit")


def get_dynamodb_resource():
    return boto3.resource(
        "dynamodb",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )


def get_dynamodb_table(table_name: Optional[str] = None):
    dynamodb = get_dynamodb_resource()
    name = table_name or DYNAMODB_TABLE_NAME
    return dynamodb.Table(name)


def create_audit_table(
    table_name: Optional[str] = None,
    billing_mode: str = "PAY_PER_REQUEST",
) -> dict:
    dynamodb = get_dynamodb_resource()
    name = table_name or DYNAMODB_TABLE_NAME

    try:
        table = dynamodb.create_table(
            TableName=name,
            KeySchema=[
                {"AttributeName": "event_id", "KeyType": "HASH"},
                {"AttributeName": "timestamp", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "event_id", "AttributeType": "S"},
                {"AttributeName": "timestamp", "AttributeType": "S"},
                {"AttributeName": "user_sub", "AttributeType": "S"},
                {"AttributeName": "provider", "AttributeType": "S"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "UserSubIndex",
                    "KeySchema": [
                        {"AttributeName": "user_sub", "KeyType": "HASH"},
                        {"AttributeName": "timestamp", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "BillingMode": billing_mode,
                },
                {
                    "IndexName": "ProviderIndex",
                    "KeySchema": [
                        {"AttributeName": "provider", "KeyType": "HASH"},
                        {"AttributeName": "timestamp", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "BillingMode": billing_mode,
                },
            ],
            BillingMode=billing_mode,
        )
        table.wait_until_exists()
        return {"status": "created", "table_name": name}
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            return {"status": "exists", "table_name": name}
        raise


def persist_audit_event(
    event: AuditEvent,
    table_name: Optional[str] = None,
) -> dict:
    table = get_dynamodb_table(table_name)

    if not event.event_id:
        event.event_id = str(uuid.uuid4())
    if not event.timestamp:
        event.timestamp = datetime.now(timezone.utc).isoformat()

    item = {
        "event_id": event.event_id,
        "timestamp": event.timestamp,
        "event_type": event.event_type,
        "user_sub": event.user_sub,
        "provider": event.provider,
        "client_id": event.client_id,
        "ip_address": event.ip_address,
        "user_agent": event.user_agent,
        "status": event.status,
        "details": event.details,
        "risk_score": event.risk_score,
        "moderation_flags": event.moderation_flags,
    }

    response = table.put_item(Item=item)

    return {
        "status": "persisted",
        "event_id": event.event_id,
        "table_name": table.table_name,
        "response_metadata": response.get("ResponseMetadata", {}),
    }


def persist_audit_events_batch(
    events: List[AuditEvent],
    table_name: Optional[str] = None,
) -> dict:
    table = get_dynamodb_table(table_name)

    items = []
    for event in events:
        if not event.event_id:
            event.event_id = str(uuid.uuid4())
        if not event.timestamp:
            event.timestamp = datetime.now(timezone.utc).isoformat()

        items.append(
            {
                "event_id": event.event_id,
                "timestamp": event.timestamp,
                "event_type": event.event_type,
                "user_sub": event.user_sub,
                "provider": event.provider,
                "client_id": event.client_id,
                "ip_address": event.ip_address,
                "user_agent": event.user_agent,
                "status": event.status,
                "details": event.details,
                "risk_score": event.risk_score,
                "moderation_flags": event.moderation_flags,
            }
        )

    persisted = 0
    failed = 0
    errors = []

    for i in range(0, len(items), 25):
        batch = items[i : i + 25]
        request_items = {
            table.table_name: [{"PutRequest": {"Item": item}} for item in batch]
        }

        response = table.meta.client.batch_write_item(RequestItems=request_items)

        unprocessed = response.get("UnprocessedItems", {})
        if unprocessed:
            failed += len(unprocessed.get(table.table_name, []))
            errors.append("Some items were not processed")

        persisted += len(batch) - len(unprocessed.get(table.table_name, []))

    return {
        "status": "batch_completed",
        "total": len(items),
        "persisted": persisted,
        "failed": failed,
        "errors": errors,
        "table_name": table.table_name,
    }


def query_events_by_user(
    user_sub: str,
    table_name: Optional[str] = None,
    limit: int = 50,
) -> List[dict]:
    table = get_dynamodb_table(table_name)

    response = table.query(
        IndexName="UserSubIndex",
        KeyConditionExpression=Key("user_sub").eq(user_sub),
        Limit=limit,
        ScanIndexForward=False,
    )

    return response.get("Items", [])


def query_events_by_provider(
    provider: str,
    table_name: Optional[str] = None,
    limit: int = 50,
) -> List[dict]:
    table = get_dynamodb_table(table_name)

    response = table.query(
        IndexName="ProviderIndex",
        KeyConditionExpression=Key("provider").eq(provider),
        Limit=limit,
        ScanIndexForward=False,
    )

    return response.get("Items", [])


def query_events_by_time_range(
    start_time: str,
    end_time: str,
    table_name: Optional[str] = None,
    limit: int = 100,
) -> List[dict]:
    table = get_dynamodb_table(table_name)

    response = table.query(
        KeyConditionExpression=Key("timestamp").between(start_time, end_time),
        Limit=limit,
        ScanIndexForward=True,
    )

    return response.get("Items", [])


def get_event_by_id(
    event_id: str,
    table_name: Optional[str] = None,
) -> Optional[dict]:
    table = get_dynamodb_table(table_name)

    response = table.query(
        KeyConditionExpression=Key("event_id").eq(event_id),
        Limit=1,
    )

    items = response.get("Items", [])
    return items[0] if items else None


def delete_audit_event(
    event_id: str,
    timestamp: str,
    table_name: Optional[str] = None,
) -> dict:
    table = get_dynamodb_table(table_name)

    response = table.delete_item(
        Key={
            "event_id": event_id,
            "timestamp": timestamp,
        }
    )

    return {
        "status": "deleted",
        "event_id": event_id,
        "table_name": table.table_name,
    }

"""
Persist federated-login audit records in Amazon DynamoDB.

Stores OAuth/OIDC login events, token exchanges, profile fetches,
and authentication failures in a managed DynamoDB table for
auditing, compliance, and analytics purposes.
"""

import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError


AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
AUDIT_TABLE_NAME = os.environ.get(
    "FEDERATED_LOGIN_AUDIT_TABLE",
    "federated-login-audit",
)


class AuditStoreError(Exception):
    """Raised when audit record storage or retrieval fails."""
    pass


def create_dynamodb_client(region: Optional[str] = None):
    """Create a boto3 DynamoDB client."""
    return boto3.client(
        "dynamodb",
        region_name=region or AWS_REGION,
    )


def create_dynamodb_resource(region: Optional[str] = None):
    """Create a boto3 DynamoDB resource for high-level table operations."""
    return boto3.resource(
        "dynamodb",
        region_name=region or AWS_REGION,
    )


def create_audit_table(
    table_name: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create the federated-login audit DynamoDB table if it does not exist.

    The table uses a composite key:
    - partition_key: user_id (string)
    - sort_key: event_timestamp (string, ISO format)

    Also includes a global secondary index (GSI) on event_type for
    querying by event category.
    """
    client = create_dynamodb_client(region)
    tname = table_name or AUDIT_TABLE_NAME

    try:
        response = client.create_table(
            TableName=tname,
            KeySchema=[
                {"AttributeName": "user_id", "KeyType": "HASH"},
                {"AttributeName": "event_timestamp", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "user_id", "AttributeType": "S"},
                {"AttributeName": "event_timestamp", "AttributeType": "S"},
                {"AttributeName": "event_type", "AttributeType": "S"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "event_type_index",
                    "KeySchema": [
                        {"AttributeName": "event_type", "KeyType": "HASH"},
                        {"AttributeName": "event_timestamp", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                }
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
            Tags=[
                {"Key": "Application", "Value": "FederatedLogin"},
                {"Key": "Environment", "Value": os.environ.get("ENV", "production")},
            ],
        )
        return response
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ResourceInUseException":
            return {"status": "table_already_exists", "table_name": tname}
        raise


def store_audit_event(
    event: Dict[str, Any],
    table_name: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Store a federated-login audit event in DynamoDB.

    Persists login, logout, token exchange, profile fetch, and
    authentication failure events with full audit trail metadata.

    Expected event fields:
    - user_id: Federated user identifier (sub claim)
    - event_type: Category (login_success, login_failure, token_exchange,
      profile_fetch, logout, consent_granted, consent_denied)
    - provider: Auth0 connection/provider name
    - event_timestamp: ISO 8601 timestamp
    - ip_address: Client IP address
    - user_agent: Client user agent string
    - details: Additional event metadata

    Returns:
        DynamoDB response metadata including consumed capacity.
    """
    dynamodb = create_dynamodb_resource(region)
    tname = table_name or AUDIT_TABLE_NAME
    table = dynamodb.Table(tname)

    event_id = event.get("event_id", str(uuid.uuid4()))
    user_id = event["user_id"]
    timestamp = event.get("event_timestamp", datetime.now(timezone.utc).isoformat())

    item = {
        "event_id": event_id,
        "user_id": user_id,
        "event_timestamp": timestamp,
        "event_type": event.get("event_type", "unknown"),
        "provider": event.get("provider", "unknown"),
        "ip_address": event.get("ip_address", ""),
        "user_agent": event.get("user_agent", ""),
        "location": event.get("location", ""),
        "success": event.get("success", True),
        "details": event.get("details", {}),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "ttl": int((datetime.now(timezone.utc).timestamp()) + 7776000),
    }

    try:
        response = table.put_item(
            Item=item,
            ConditionExpression="attribute_not_exists(event_id)",
            ReturnConsumedCapacity="TOTAL",
        )
        return {
            "status": "stored",
            "event_id": event_id,
            "user_id": user_id,
            "consumed_capacity": response.get("ConsumedCapacity", {}),
        }
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return {"status": "duplicate", "event_id": event_id}
        raise AuditStoreError(f"DynamoDB put failed: {exc}") from exc


def query_user_audit_events(
    user_id: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    event_type: Optional[str] = None,
    limit: int = 100,
    table_name: Optional[str] = None,
    region: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Query audit events for a specific user from DynamoDB.

    Supports filtering by time range and event type. Uses DynamoDB's
    Query API with key conditions for efficient retrieval.

    Args:
        user_id: The federated user's identifier (partition key).
        start_time: ISO 8601 start of time range (sort key lower bound).
        end_time: ISO 8601 end of time range (sort key upper bound).
        event_type: Filter by event type (uses GSI scan if specified).
        limit: Maximum number of events to return.
        table_name: DynamoDB table name override.
        region: AWS region override.

    Returns:
        List of audit event records.
    """
    dynamodb = create_dynamodb_resource(region)
    tname = table_name or AUDIT_TABLE_NAME
    table = dynamodb.Table(tname)

    if event_type:
        response = table.query(
            IndexName="event_type_index",
            KeyConditionExpression=Key("event_type").eq(event_type),
            ScanIndexForward=False,
            Limit=limit,
        )
    else:
        key_condition = Key("user_id").eq(user_id)
        if start_time and end_time:
            key_condition &= Key("event_timestamp").between(start_time, end_time)
        elif start_time:
            key_condition &= Key("event_timestamp").gte(start_time)
        elif end_time:
            key_condition &= Key("event_timestamp").lte(end_time)

        response = table.query(
            KeyConditionExpression=key_condition,
            ScanIndexForward=False,
            Limit=limit,
        )

    return response.get("Items", [])


def store_login_event(
    user_id: str,
    provider: str,
    success: bool,
    ip_address: str = "",
    user_agent: str = "",
    details: Optional[Dict[str, Any]] = None,
    table_name: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Store a federated login event in DynamoDB.

    Convenience wrapper for storing login_success or login_failure
    events with Auth0 provider context.
    """
    event_type = "login_success" if success else "login_failure"
    event = {
        "event_id": str(uuid.uuid4()),
        "user_id": user_id,
        "event_type": event_type,
        "provider": provider,
        "event_timestamp": datetime.now(timezone.utc).isoformat(),
        "ip_address": ip_address,
        "user_agent": user_agent,
        "success": success,
        "details": details or {},
    }

    return store_audit_event(event, table_name=table_name, region=region)


def store_token_exchange_event(
    user_id: str,
    provider: str,
    grant_type: str = "authorization_code",
    success: bool = True,
    details: Optional[Dict[str, Any]] = None,
    table_name: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Store a token exchange event in DynamoDB.

    Records when an authorization code is exchanged for tokens via
    the Auth0 /oauth/token endpoint, useful for auditing token
    issuance patterns.
    """
    event = {
        "event_id": str(uuid.uuid4()),
        "user_id": user_id,
        "event_type": "token_exchange",
        "provider": provider,
        "event_timestamp": datetime.now(timezone.utc).isoformat(),
        "success": success,
        "details": {
            "grant_type": grant_type,
            **(details or {}),
        },
    }

    return store_audit_event(event, table_name=table_name, region=region)


def get_audit_statistics(
    user_id: Optional[str] = None,
    days: int = 30,
    table_name: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Compute audit statistics from DynamoDB for a user or globally.

    Returns counts by event type, success/failure rates, and
    provider distribution for the specified time period.
    """
    dynamodb = create_dynamodb_resource(region)
    tname = table_name or AUDIT_TABLE_NAME
    table = dynamodb.Table(tname)

    cutoff = (
        datetime.now(timezone.utc) - __import__("datetime").timedelta(days=days)
    ).isoformat()

    stats = {
        "total_events": 0,
        "by_type": {},
        "by_provider": {},
        "success_count": 0,
        "failure_count": 0,
        "time_period_days": days,
    }

    if user_id:
        response = table.query(
            KeyConditionExpression=Key("user_id").eq(user_id)
            & Key("event_timestamp").gte(cutoff),
            ScanIndexForward=False,
            Limit=1000,
        )
    else:
        response = table.scan(
            FilterExpression=Attr("event_timestamp").gte(cutoff),
            Limit=1000,
        )

    for item in response.get("Items", []):
        stats["total_events"] += 1

        etype = item.get("event_type", "unknown")
        stats["by_type"][etype] = stats["by_type"].get(etype, 0) + 1

        prov = item.get("provider", "unknown")
        stats["by_provider"][prov] = stats["by_provider"].get(prov, 0) + 1

        if item.get("success", True):
            stats["success_count"] += 1
        else:
            stats["failure_count"] += 1

    return stats


if __name__ == "__main__":
    print("DynamoDB federated-login audit store ready.")
    print(f"Table: {AUDIT_TABLE_NAME}")
    print(f"Region: {AWS_REGION}")

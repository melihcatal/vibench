"""
[LATER-STEP] Persist federated-login audit records in Amazon DynamoDB.

Uses the AWS SDK (boto3) to store and query federated login audit events in
a managed DynamoDB document table (service=Amazon DynamoDB).

Table schema:
  - Partition key: partition_key (string) - composite of provider#event_type
  - Sort key: event_id (string) - UUID of the audit event
  - GSI: by_sub (hash=sub, range=timestamp)
  - GSI: by_timestamp (hash=partition_key, range=timestamp)

Required env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import json
import logging
import time
from typing import Any, Dict, List, Optional

import boto3
from boto3.dynamodb.conditions import Key

from identity_models import AuditEvent

logger = logging.getLogger(__name__)

TABLE_NAME_DEFAULT = "federated-login-audit"


class DynamoDBAuditStore:
    """
    Persistence layer for federated login audit events in Amazon DynamoDB.

    Uses boto3 DynamoDB service client:
        https://dynamodb.{region}.amazonaws.com
    """

    def __init__(
        self,
        table_name: Optional[str] = None,
        region_name: Optional[str] = None,
        endpoint_url: Optional[str] = None,
    ):
        self.table_name = table_name or TABLE_NAME_DEFAULT
        self.region_name = region_name

        dynamodb_kwargs: Dict[str, Any] = {"region_name": self.region_name}
        if endpoint_url:
            dynamodb_kwargs["endpoint_url"] = endpoint_url

        self.dynamodb = boto3.resource("dynamodb", **dynamodb_kwargs)
        self.client = boto3.client("dynamodb", **dynamodb_kwargs)
        self.table = self.dynamodb.Table(self.table_name)

    def ensure_table_exists(self, billing_mode: str = "PAY_PER_REQUEST") -> None:
        """Create the DynamoDB table if it does not already exist."""
        try:
            self.table.load()
            logger.info("DynamoDB table '%s' already exists.", self.table_name)
        except self.client.exceptions.ResourceNotFoundException:
            logger.info("Creating DynamoDB table '%s'...", self.table_name)
            self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {"AttributeName": "partition_key", "KeyType": "HASH"},
                    {"AttributeName": "event_id", "KeyType": "RANGE"},
                ],
                AttributeDefinitions=[
                    {"AttributeName": "partition_key", "AttributeType": "S"},
                    {"AttributeName": "event_id", "AttributeType": "S"},
                    {"AttributeName": "sub", "AttributeType": "S"},
                    {"AttributeName": "timestamp", "AttributeType": "N"},
                ],
                GlobalSecondaryIndexes=[
                    {
                        "IndexName": "by_sub",
                        "KeySchema": [
                            {"AttributeName": "sub", "KeyType": "HASH"},
                            {"AttributeName": "timestamp", "KeyType": "RANGE"},
                        ],
                        "Projection": {"ProjectionType": "ALL"},
                        "BillingMode": billing_mode,
                    },
                    {
                        "IndexName": "by_timestamp",
                        "KeySchema": [
                            {"AttributeName": "partition_key", "KeyType": "HASH"},
                            {"AttributeName": "timestamp", "KeyType": "RANGE"},
                        ],
                        "Projection": {"ProjectionType": "ALL"},
                        "BillingMode": billing_mode,
                    },
                ],
                BillingMode=billing_mode,
            )
            self.table.wait_until_exists()
            logger.info("DynamoDB table '%s' created successfully.", self.table_name)

    def store_event(self, event: AuditEvent) -> Dict[str, Any]:
        """
        Persist a single AuditEvent to DynamoDB.

        partition_key = "{provider}#{event_type}"
        sort key = event_id
        """
        partition_key = f"{event.provider}#{event.event_type}"

        item: Dict[str, Any] = {
            "partition_key": partition_key,
            "event_id": event.event_id,
            "timestamp": event.timestamp,
            "event_type": event.event_type,
            "sub": event.sub,
            "email": event.email,
            "provider": event.provider,
            "ip_address": event.ip_address,
            "user_agent": event.user_agent,
            "state": event.state,
            "details": json.dumps(event.details) if event.details else "",
            "notes": event.notes,
        }

        response = self.table.put_item(Item=item)

        logger.info(
            "Stored audit event in DynamoDB: partition_key=%s, event_id=%s",
            partition_key,
            event.event_id,
        )

        return response

    def store_events(self, events: List[AuditEvent]) -> List[Dict[str, Any]]:
        """Persist multiple audit events using batch_write."""
        if not events:
            return []

        with self.table.batch_writer() as batch:
            for event in events:
                partition_key = f"{event.provider}#{event.event_type}"
                item: Dict[str, Any] = {
                    "partition_key": partition_key,
                    "event_id": event.event_id,
                    "timestamp": event.timestamp,
                    "event_type": event.event_type,
                    "sub": event.sub,
                    "email": event.email,
                    "provider": event.provider,
                    "ip_address": event.ip_address,
                    "user_agent": event.user_agent,
                    "state": event.state,
                    "details": json.dumps(event.details) if event.details else "",
                    "notes": event.notes,
                }
                batch.put_item(Item=item)

        logger.info("Batch stored %d audit events in DynamoDB.", len(events))
        return []

    def get_event(self, event_id: str, provider: str, event_type: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single audit event by its keys."""
        partition_key = f"{provider}#{event_type}"
        try:
            response = self.table.get_item(
                Key={"partition_key": partition_key, "event_id": event_id}
            )
            return response.get("Item")
        except self.client.exceptions.ResourceNotFoundException:
            return None

    def query_by_sub(
        self, sub: str, start_time: Optional[float] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Query audit events for a specific user (sub) using the by_sub GSI.
        """
        query_kwargs: Dict[str, Any] = {
            "IndexName": "by_sub",
            "KeyConditionExpression": Key("sub").eq(sub),
            "ScanIndexForward": False,  # newest first
            "Limit": limit,
        }

        if start_time is not None:
            query_kwargs["KeyConditionExpression"] = Key("sub").eq(sub) & Key("timestamp").gte(
                str(start_time)
            )

        response = self.table.query(**query_kwargs)
        items = response.get("Items", [])

        # Parse details back from JSON string
        for item in items:
            if item.get("details") and isinstance(item["details"], str):
                try:
                    item["details"] = json.loads(item["details"])
                except json.JSONDecodeError:
                    pass

        return items

    def query_by_provider_and_type(
        self,
        provider: str,
        event_type: str,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Query audit events by provider and event type with optional time range.
        """
        partition_key = f"{provider}#{event_type}"
        query_kwargs: Dict[str, Any] = {
            "KeyConditionExpression": Key("partition_key").eq(partition_key),
            "ScanIndexForward": False,
            "Limit": limit,
        }

        if start_time is not None and end_time is not None:
            query_kwargs["KeyConditionExpression"] = (
                Key("partition_key").eq(partition_key)
                & Key("timestamp").between(str(start_time), str(end_time))
            )
        elif start_time is not None:
            query_kwargs["KeyConditionExpression"] = (
                Key("partition_key").eq(partition_key)
                & Key("timestamp").gte(str(start_time))
            )

        response = self.table.query(**query_kwargs)
        items = response.get("Items", [])

        for item in items:
            if item.get("details") and isinstance(item["details"], str):
                try:
                    item["details"] = json.loads(item["details"])
                except json.JSONDecodeError:
                    pass

        return items

    def get_event_stats(
        self, provider: Optional[str] = None, event_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get aggregate statistics from DynamoDB.

        Note: DynamoDB requires a scan for full aggregation; this is best for
        small datasets or should use a materialized view for large ones.
        """
        scan_kwargs: Dict[str, Any] = {}
        if provider and event_type:
            scan_kwargs["FilterExpression"] = (
                "provider = :p AND event_type = :e"
            )
            scan_kwargs["ExpressionAttributeValues"] = {
                ":p": provider,
                ":e": event_type,
            }
        elif provider:
            scan_kwargs["FilterExpression"] = "provider = :p"
            scan_kwargs["ExpressionAttributeValues"] = {":p": provider}
        elif event_type:
            scan_kwargs["FilterExpression"] = "event_type = :e"
            scan_kwargs["ExpressionAttributeValues"] = {":e": event_type}

        total_events = 0
        unique_users = set()
        event_types: Dict[str, int] = {}

        response = self.table.scan(**scan_kwargs)
        for item in response.get("Items", []):
            total_events += 1
            if item.get("sub"):
                unique_users.add(item["sub"])
            et = item.get("event_type", "unknown")
            event_types[et] = event_types.get(et, 0) + 1

        return {
            "total_events": total_events,
            "unique_users": len(unique_users),
            "event_type_counts": event_types,
            "provider": "dynamodb",
            "table_name": self.table_name,
        }


def persist_audit_events(
    events: List[AuditEvent],
    table_name: Optional[str] = None,
    region_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convenience function: store audit events in DynamoDB.
    """
    store = DynamoDBAuditStore(table_name=table_name, region_name=region_name)
    store.ensure_table_exists()
    store.store_events(events)

    return {
        "success": True,
        "events_stored": len(events),
        "table_name": store.table_name,
        "provider": "dynamodb",
    }

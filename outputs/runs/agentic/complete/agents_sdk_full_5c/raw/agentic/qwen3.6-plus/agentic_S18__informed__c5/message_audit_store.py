"""Persist processed message records for later lookup using Amazon DynamoDB.

Uses the boto3 SDK to write and retrieve AuditRecord entries in an
Amazon DynamoDB table. Authentication relies on AWS_ACCESS_KEY_ID
and AWS_SECRET_ACCESS_KEY.
"""

import os
import time
from typing import Any, Dict, List, Optional

import boto3
from boto3.dynamodb.conditions import Key as DynamoKey

from messaging_models import ConsumedMessage, AuditRecord, build_audit_record_from_message


# DynamoDB table name for audit records
DYNAMODB_TABLE = os.environ.get("AUDIT_TABLE_NAME", "message-audit-store")
DYNAMODB_REGION = os.environ.get("AWS_REGION", "us-east-1")


def _get_dynamodb_resource():
    """Create or retrieve a boto3 DynamoDB resource."""
    return boto3.resource(
        "dynamodb",
        region_name=DYNAMODB_REGION,
    )


def _get_dynamodb_table():
    """Return the DynamoDB Table handle for audit records."""
    dynamodb = _get_dynamodb_resource()
    return dynamodb.Table(DYNAMODB_TABLE)


def store_audit_record(record: AuditRecord) -> Dict[str, Any]:
    """Persist an AuditRecord to Amazon DynamoDB.

    The record_id field is used as the partition key.

    Args:
        record: The AuditRecord to persist.

    Returns:
        The low-level response metadata from DynamoDB put_item.
    """
    table = _get_dynamodb_table()

    item: Dict[str, Any] = {
        "record_id": record.record_id,
        "message_id": record.message_id,
        "event_id": record.event_id,
        "event_type": record.event_type,
        "source": record.source,
        "payload": record.payload,
        "status": record.status,
        "processed_at": record.processed_at,
    }
    if record.summary_text:
        item["summary_text"] = record.summary_text
    if record.translation:
        item["translation"] = record.translation
    if record.safety_flags:
        item["safety_flags"] = record.safety_flags
    if record.extra_metadata:
        item["extra_metadata"] = record.extra_metadata

    response = table.put_item(Item=item)
    return response


def store_from_consumed_message(
    message: ConsumedMessage,
    status: str = "processed",
    summary_text: Optional[str] = None,
    translation: Optional[str] = None,
    safety_flags: Optional[List[str]] = None,
    extra_metadata: Optional[Dict[str, Any]] = None,
) -> AuditRecord:
    """Build an AuditRecord from a ConsumedMessage and store it in DynamoDB.

    Args:
        message: The consumed message to record.
        status: Processing status string.
        summary_text: Optional summary text.
        translation: Optional translated text.
        safety_flags: Optional list of safety flag categories.
        extra_metadata: Optional additional metadata dict.

    Returns:
        The AuditRecord that was persisted.
    """
    record = build_audit_record_from_message(
        message=message,
        status=status,
        summary_text=summary_text,
        translation=translation,
        safety_flags=safety_flags,
        extra_metadata=extra_metadata,
    )
    store_audit_record(record)
    return record


def lookup_by_event_id(event_id: str) -> List[Dict[str, Any]]:
    """Query DynamoDB for all audit records matching an event_id.

    This uses a secondary index on event_id or a scan if no index exists.

    Args:
        event_id: The event_id to search for.

    Returns:
        List of matching audit record dicts.
    """
    table = _get_dynamodb_table()

    try:
        response = table.query(
            IndexName="event_id-index",
            KeyConditionExpression=DynamoKey("event_id").eq(event_id),
        )
        return response.get("Items", [])
    except Exception:
        # Fall back to a scan if the index doesn't exist
        response = table.scan(
            FilterExpression=DynamoKey("event_id").eq(event_id),
        )
        return response.get("Items", [])


def lookup_by_record_id(record_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a single audit record by its partition key record_id.

    Args:
        record_id: The primary key of the record.

    Returns:
        The record dict if found, otherwise None.
    """
    table = _get_dynamodb_table()
    response = table.get_item(Key={"record_id": record_id})
    return response.get("Item")


def list_recent_records(limit: int = 20) -> List[Dict[str, Any]]:
    """Scan DynamoDB for the most recent audit records by processed_at.

    Args:
        limit: Maximum number of records to return.

    Returns:
        List of record dicts, newest first.
    """
    table = _get_dynamodb_table()
    response = table.scan(
        Limit=limit,
    )
    items = response.get("Items", [])
    items.sort(key=lambda r: r.get("processed_at", 0), reverse=True)
    return items


if __name__ == "__main__":
    sample_msg = ConsumedMessage(
        message_id="msg-audit-1",
        event_id="evt-audit-001",
        event_type="order.placed",
        source="ecommerce",
        payload={"order_id": "ORD-555", "total": 99.99},
        attributes={},
    )
    record = store_from_consumed_message(
        sample_msg,
        status="processed",
        summary_text="Order ORD-555 processed successfully.",
    )
    print(f"Stored record_id={record.record_id}")

    found = lookup_by_record_id(record.record_id)
    if found:
        print(f"Retrieved: event_id={found.get('event_id')}")

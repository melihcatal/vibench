"""Persist processed message records for later lookup using AWS DynamoDB.

Uses the boto3 SDK to store and retrieve message processing audit records
in a managed AWS DynamoDB table for compliance and debugging.
"""

import os
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key, Attr

# AWS DynamoDB table configuration
DEFAULT_AUDIT_TABLE = os.environ.get("AUDIT_TABLE_NAME", "message-audit-store")
DEFAULT_AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")


def _serialize_dynamodb(value: Any) -> Any:
    """Convert Python types to DynamoDB-compatible types."""
    if isinstance(value, float):
        return Decimal(str(value))
    elif isinstance(value, dict):
        return {k: _serialize_dynamodb(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_serialize_dynamodb(item) for item in value]
    return value


def _deserialize_dynamodb(value: Any) -> Any:
    """Convert DynamoDB types back to Python types."""
    if isinstance(value, Decimal):
        return float(value)
    elif isinstance(value, dict):
        return {k: _deserialize_dynamodb(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_deserialize_dynamodb(item) for item in value]
    return value


def store_message_audit(
    event_id: str,
    message_data: Dict[str, Any],
    processing_result: Dict[str, Any],
    table_name: Optional[str] = None,
    aws_region: Optional[str] = None,
) -> Dict[str, Any]:
    """Store a processed message record in AWS DynamoDB for audit.

    Args:
        event_id: Unique event identifier (used as partition key).
        message_data: Original message payload and metadata.
        processing_result: Result of processing the message.
        table_name: DynamoDB table name. Defaults from env.
        aws_region: AWS region. Defaults from env.

    Returns:
        Dict with storage confirmation.
    """
    region = aws_region or os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
    table = table_name or os.environ.get("AUDIT_TABLE_NAME", DEFAULT_AUDIT_TABLE)

    dynamodb = boto3.resource("dynamodb", region_name=region)
    audit_table = dynamodb.Table(table)

    processing_time = processing_result.get("processing_time_ms", 0)
    timestamp = processing_result.get("timestamp", datetime.now(timezone.utc).isoformat())

    record = {
        "event_id": event_id,
        "timestamp": timestamp,
        "event_type": message_data.get("event_type", processing_result.get("event_type", "unknown")),
        "processing_status": processing_result.get("status", "unknown"),
        "error_message": processing_result.get("error_message"),
        "message_data": _serialize_dynamodb(message_data),
        "processing_result": _serialize_dynamodb(processing_result),
        "stored_at": datetime.now(timezone.utc).isoformat(),
    }
    if processing_time:
        record["processing_time_ms"] = _serialize_dynamodb(processing_time)

    audit_table.put_item(Item=record)

    return {
        "status": "stored",
        "table": table,
        "event_id": event_id,
        "timestamp": timestamp,
        "region": region,
    }


def batch_store_audit(
    records: List[Dict[str, Any]],
    table_name: Optional[str] = None,
    aws_region: Optional[str] = None,
) -> Dict[str, Any]:
    """Store multiple audit records in DynamoDB using batch write.

    Args:
        records: List of dicts with event_id, message_data, processing_result.
        table_name: DynamoDB table name.
        aws_region: AWS region.

    Returns:
        Dict with batch storage results.
    """
    region = aws_region or os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
    table = table_name or os.environ.get("AUDIT_TABLE_NAME", DEFAULT_AUDIT_TABLE)

    dynamodb = boto3.resource("dynamodb", region_name=region)
    audit_table = dynamodb.Table(table)

    stored_count = 0
    failed_ids = []

    with audit_table.batch_writer() as batch:
        for record in records:
            event_id = record.get("event_id", f"unknown-{stored_count}")
            message_data = record.get("message_data", {})
            processing_result = record.get("processing_result", {})
            timestamp = processing_result.get("timestamp", datetime.now(timezone.utc).isoformat())

            item = {
                "event_id": event_id,
                "timestamp": timestamp,
                "event_type": message_data.get("event_type", processing_result.get("event_type", "unknown")),
                "processing_status": processing_result.get("status", "unknown"),
                "error_message": processing_result.get("error_message"),
                "message_data": _serialize_dynamodb(message_data),
                "processing_result": _serialize_dynamodb(processing_result),
                "stored_at": datetime.now(timezone.utc).isoformat(),
            }

            try:
                batch.put_item(Item=item)
                stored_count += 1
            except Exception:
                failed_ids.append(event_id)

    return {
        "status": "batch_stored",
        "table": table,
        "stored_count": stored_count,
        "failed_count": len(failed_ids),
        "failed_event_ids": failed_ids,
        "region": region,
    }


def lookup_message_audit(
    event_id: str,
    table_name: Optional[str] = None,
    aws_region: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Retrieve a message audit record from DynamoDB by event_id.

    Args:
        event_id: Event identifier to look up.
        table_name: DynamoDB table name.
        aws_region: AWS region.

    Returns:
        Dict with audit record or None if not found.
    """
    region = aws_region or os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
    table = table_name or os.environ.get("AUDIT_TABLE_NAME", DEFAULT_AUDIT_TABLE)

    dynamodb = boto3.resource("dynamodb", region_name=region)
    audit_table = dynamodb.Table(table)

    response = audit_table.get_item(Key={"event_id": event_id})
    item = response.get("Item")

    if item:
        return _deserialize_dynamodb(item)
    return None


def query_audit_by_status(
    status: str,
    limit: int = 50,
    table_name: Optional[str] = None,
    aws_region: Optional[str] = None,
) -> Dict[str, Any]:
    """Query audit records by processing status using DynamoDB scan.

    Args:
        status: Processing status to filter (e.g., "failed", "success").
        limit: Maximum number of records to return.
        table_name: DynamoDB table name.
        aws_region: AWS region.

    Returns:
        Dict with matching audit records.
    """
    region = aws_region or os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
    table = table_name or os.environ.get("AUDIT_TABLE_NAME", DEFAULT_AUDIT_TABLE)

    dynamodb = boto3.resource("dynamodb", region_name=region)
    audit_table = dynamodb.Table(table)

    response = audit_table.scan(
        FilterExpression=Attr("processing_status").eq(status),
        Limit=limit,
    )

    items = [_deserialize_dynamodb(item) for item in response.get("Items", [])]

    return {
        "status": "queried",
        "filter_status": status,
        "count": len(items),
        "records": items,
        "table": table,
    }


if __name__ == "__main__":
    sample_record = {
        "event_id": "audit-test-001",
        "message_data": {"event_type": "order.created", "payload": {"order_id": "ORD-999"}},
        "processing_result": {"status": "success", "timestamp": datetime.now(timezone.utc).isoformat()},
    }

    result = store_message_audit(
        event_id=sample_record["event_id"],
        message_data=sample_record["message_data"],
        processing_result=sample_record["processing_result"],
    )
    print(json.dumps(result, indent=2))

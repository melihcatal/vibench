"""
observability_client.py

Local configuration and client helper utilities for Managed Log Query / Log Ingestion
using Amazon CloudWatch Logs.
"""

import os
import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any

import boto3
from botocore.config import Config


def get_cloudwatch_logs_client() -> boto3.client:
    """
    Create and return a configured boto3 client for Amazon CloudWatch Logs.

    Required environment variables:
        AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY
    Optional:
        AWS_DEFAULT_REGION (defaults to us-east-1)
    """
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    session = boto3.Session(
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=region,
    )
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        connect_timeout=5,
        read_timeout=10,
    )
    return session.client("logs", config=config)


def build_log_event(
    message: str,
    structured_fields: Optional[Dict[str, Any]] = None,
    timestamp_ms: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Build a CloudWatch Logs put_log_events-compatible event dict.

    Args:
        message: The primary log message string.
        structured_fields: Additional key-value pairs to merge into the event.
        timestamp_ms: Epoch milliseconds; defaults to now.

    Returns:
        Dict suitable for CloudWatch put_log_events entry.
    """
    ts = timestamp_ms or int(datetime.now(timezone.utc).timestamp() * 1000)
    payload = {
        "timestamp": ts,
        "message": message,
    }
    if structured_fields:
        payload.update(structured_fields)
    return payload


def ensure_log_group(
    client: boto3.client,
    log_group_name: str,
    retention_days: int = 14,
) -> None:
    """
    Ensure the named CloudWatch log group exists; create if missing.
    """
    try:
        client.describe_log_groups(logGroupNamePrefix=log_group_name)
    except client.exceptions.ResourceNotFoundException:
        client.create_log_group(
            logGroupName=log_group_name,
        )
    client.put_retention_policy(
        logGroupName=log_group_name,
        retentionInDays=retention_days,
    )


def ensure_log_stream(
    client: boto3.client,
    log_group_name: str,
    log_stream_name: str,
) -> None:
    """
    Ensure the named log stream exists within the group; create if missing.
    """
    try:
        client.create_log_stream(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
        )
    except client.exceptions.ResourceAlreadyExistsException:
        pass


def get_sequence_token(
    client: boto3.client,
    log_group_name: str,
    log_stream_name: str,
) -> Optional[str]:
    """
    Fetch the current sequence token for a log stream (required for put_log_events).
    Returns None for a brand-new stream.
    """
    try:
        resp = client.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name,
            limit=1,
        )
        streams = resp.get("logStreams", [])
        if streams:
            return streams[0].get("uploadSequenceToken")
    except Exception:
        pass
    return None


def put_log_events_batch(
    client: boto3.client,
    log_group_name: str,
    log_stream_name: str,
    events: List[Dict[str, Any]],
) -> Optional[str]:
    """
    Submit a batch of log events to CloudWatch Logs, handling sequence tokens.

    Args:
        client: boto3 CloudWatch Logs client.
        log_group_name: Target log group.
        log_stream_name: Target log stream.
        events: List of event dicts with 'timestamp' and 'message' keys.

    Returns:
        The next sequence token for subsequent calls.
    """
    ensure_log_group(client, log_group_name)
    ensure_log_stream(client, log_group_name, log_stream_name)

    seq_token = get_sequence_token(client, log_group_name, log_stream_name)

    kwargs = {
        "logGroupName": log_group_name,
        "logStreamName": log_stream_name,
        "logEvents": events,
    }
    if seq_token:
        kwargs["sequenceToken"] = seq_token

    try:
        resp = client.put_log_events(**kwargs)
        return resp.get("nextSequenceToken")
    except client.exceptions.InvalidSequenceTokenException as exc:
        # Retry once with the expected token from the exception message.
        expected = exc.response["Error"]["Message"].split(":")[-1].strip()
        kwargs["sequenceToken"] = expected
        resp = client.put_log_events(**kwargs)
        return resp.get("nextSequenceToken")


def generate_correlation_id() -> str:
    """Generate a UUIDv4 correlation / request identifier string."""
    return str(uuid.uuid4())


def build_time_filter(
    hours_back: int = 1,
) -> tuple:
    """
    Build start/end epoch-ms for a time window.

    Returns:
        (start_ms, end_ms)
    """
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=hours_back)
    return (int(start.timestamp() * 1000), int(now.timestamp() * 1000))

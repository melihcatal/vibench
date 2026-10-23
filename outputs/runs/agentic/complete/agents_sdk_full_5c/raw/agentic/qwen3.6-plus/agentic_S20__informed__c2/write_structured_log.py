"""
write_structured_log.py

Writes a structured JSON log event to Amazon CloudWatch Logs
using the aws cloudwatch logs SDK (boto3).
"""

import os
import json
from observability_client import (
    get_cloudwatch_logs_client,
    build_log_event,
    put_log_events_batch,
)
from observability_models import LogEvent


def write_structured_log(
    log_group_name: str,
    log_stream_name: str,
    level: str,
    message: str,
    service: str,
    extra_fields: dict | None = None,
) -> str | None:
    """
    Write a single structured JSON log event to Amazon CloudWatch Logs.

    Args:
        log_group_name: CloudWatch log group name.
        log_stream_name: CloudWatch log stream name.
        level: Log severity (INFO, WARN, ERROR, etc.).
        message: Human-readable log message.
        service: Service name for the event.
        extra_fields: Optional additional structured key/value pairs.

    Returns:
        The next sequence token after the write, or None on failure.
    """
    structured = {
        "level": level,
        "service": service,
    }
    if extra_fields:
        structured.update(extra_fields)

    event = LogEvent(message=message, structured_fields=structured)
    cw_event = event.to_cloudwatch_event()

    client = get_cloudwatch_logs_client()
    seq_token = put_log_events_batch(
        client=client,
        log_group_name=log_group_name,
        log_stream_name=log_stream_name,
        events=[cw_event],
    )
    return seq_token


if __name__ == "__main__":
    lg = os.environ.get("CLOUDWATCH_LOG_GROUP", "/app/production")
    ls = os.environ.get("CLOUDWATCH_LOG_STREAM", "api-server")
    token = write_structured_log(
        log_group_name=lg,
        log_stream_name=ls,
        level="INFO",
        message="Application started successfully",
        service="payment-api",
        extra_fields={"version": "2.4.1", "region": "us-east-1"},
    )
    print(f"Wrote structured log event, next sequence token: {token}")

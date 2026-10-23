"""
write_correlated_logs.py

Writes application log events that include a shared request or correlation
identifier to Amazon CloudWatch Logs using the boto3 SDK.
"""

import os
from typing import List, Optional
from observability_client import (
    get_cloudwatch_logs_client,
    generate_correlation_id,
    put_log_events_batch,
)
from observability_models import LogEvent, CorrelatedLogGroup


def write_correlated_logs(
    log_group_name: str,
    log_stream_name: str,
    messages: List[str],
    correlation_id: Optional[str] = None,
    service: str = "default-service",
    extra_fields: dict | None = None,
) -> str | None:
    """
    Write a group of log events sharing a correlation/trace ID
    to Amazon CloudWatch Logs.

    Args:
        log_group_name: CloudWatch log group name.
        log_stream_name: CloudWatch log stream name.
        messages: List of log message strings to write.
        correlation_id: Shared request ID. Auto-generated if omitted.
        service: Service name attached to each event.
        extra_fields: Optional extra structured fields.

    Returns:
        The next sequence token after the write.
    """
    if not correlation_id:
        correlation_id = generate_correlation_id()

    group = CorrelatedLogGroup(correlation_id=correlation_id)

    for msg in messages:
        fields = {"service": service}
        if extra_fields:
            fields.update(extra_fields)
        event = LogEvent(message=msg, structured_fields=fields)
        group.add_event(event)

    cw_events = [e.to_cloudwatch_event() for e in group.events]

    client = get_cloudwatch_logs_client()
    seq_token = put_log_events_batch(
        client=client,
        log_group_name=log_group_name,
        log_stream_name=log_stream_name,
        events=cw_events,
    )
    return seq_token


if __name__ == "__main__":
    lg = os.environ.get("CLOUDWATCH_LOG_GROUP", "/app/production")
    ls = os.environ.get("CLOUDWATCH_LOG_STREAM", "api-server")
    token = write_correlated_logs(
        log_group_name=lg,
        log_stream_name=ls,
        messages=[
            "Received POST /orders request",
            "Validating payment payload",
            "Calling payment-gateway downstream API",
            "Response received: 200 OK",
            "Order persisted to database",
        ],
        service="order-service",
        extra_fields={"trace_id": "req-abc-123"},
    )
    print(f"Wrote correlated log group, next sequence token: {token}")

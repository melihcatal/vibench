"""
[SAME-SCENARIO] Writes application log events that include a shared request or correlation identifier.

Uses the Datadog HTTP Log Intake API v2 to send correlated log entries sharing
the same correlation_id for request tracing across services.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from observability_models import LogEvent, generate_correlation_id
from observability_client import send_logs_to_datadog


def write_correlated_logs(
    messages: List[str],
    status: str = "info",
    service: str = "web-app",
    correlation_id: Optional[str] = None,
    custom_attributes: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Write multiple log events that share the same correlation identifier to Datadog.

    Each log message is sent as a separate Datadog log event but tagged with
    the same correlation_id for distributed request tracing.

    Args:
        messages: List of log messages to send as correlated events.
        status: Severity level for all events.
        service: Service name for grouping logs.
        correlation_id: Shared trace/correlation ID. Generated if not provided.
        custom_attributes: Additional attributes applied to all events.

    Returns:
        Response metadata from Datadog log ingestion.
    """
    cid = correlation_id or generate_correlation_id()

    log_events = []
    for msg in messages:
        event = LogEvent(
            message=msg,
            status=status,
            service=service,
            correlation_id=cid,
            custom_attributes=custom_attributes or {},
        )
        log_events.append(event.to_payload())

    result = send_logs_to_datadog(log_events)
    result["correlation_id"] = cid
    return result


def write_request_trace_logs(
    request_id: str,
    service: str,
    request_start: Optional[str] = None,
    request_end: Optional[str] = None,
    status_code: int = 200,
    method: str = "GET",
    url: str = "/",
    duration_ms: Optional[float] = None,
    error_message: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Write a correlated set of request lifecycle logs to Datadog.

    Creates start, processing, and completion log entries all sharing the
    same request_id as the correlation identifier.
    """
    now = datetime.now(timezone.utc)
    messages = []

    messages.append(f"Request {request_id} started: {method} {url}")
    if request_start:
        messages.append(f"Request {request_id} received at {request_start}")

    if request_end:
        messages.append(f"Request {request_id} completed at {request_end}")

    if error_message:
        messages.append(f"Request {request_id} error: {error_message}")

    attrs = {
        "http.request_id": request_id,
        "http.method": method,
        "http.url": url,
        "http.status_code": status_code,
        "timestamp_start": request_start or now.isoformat(),
    }
    if duration_ms is not None:
        attrs["duration_ms"] = duration_ms
    if request_end:
        attrs["timestamp_end"] = request_end

    status = "error" if error_message else "info"
    return write_correlated_logs(
        messages=messages,
        status=status,
        service=service,
        correlation_id=request_id,
        custom_attributes=attrs,
    )


def main() -> None:
    """Example: write correlated request logs to Datadog."""
    request_id = "req-abc123-def456"
    result = write_request_trace_logs(
        request_id=request_id,
        service="payment-service",
        method="POST",
        url="/api/v1/payments",
        status_code=200,
        duration_ms=245.7,
    )
    print(json.dumps(result, indent=2))
    if not result.get("ok"):
        print(f"Failed to write correlated logs: {result.get('content')}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

"""
Writes application log events that include a shared request or correlation identifier.

Uses the Datadog Logs API (api.datadoghq.com) via the datadog-api-client SDK
to ingest correlated log events using HTTPLog/HTTPLogs with a shared
correlation_id for request tracing across service boundaries.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from observability_models import StructuredLogEvent, LogLevel, generate_correlation_id
from observability_client import ingest_log_events

DATADOG_API_HOST = "https://api.datadoghq.com"


def write_correlated_logs(
    correlation_id: Optional[str] = None,
    service: str = "my-application",
    environment: str = "production",
    events: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Write multiple correlated log events sharing a correlation ID to Datadog.

    All events share the same correlation_id to enable tracing a single
    request or transaction across multiple services or components in
    the Datadog managed logging service at api.datadoghq.com.

    Args:
        correlation_id: Shared identifier for all events. Generated if not provided.
        service: The service name emitting the logs.
        environment: Deployment environment.
        events: List of event dicts with keys: message, level, attributes.

    Returns:
        Dict with ingestion status and correlation metadata.
    """
    corr_id = correlation_id or generate_correlation_id("req")

    default_events = [
        {"message": "Request received", "level": "info", "attributes": {"http.method": "GET", "http.url": "/api/data"}},
        {"message": "Authentication validated", "level": "info", "attributes": {"auth.provider": "oauth2"}},
        {"message": "Database query executed", "level": "debug", "attributes": {"db.operation": "SELECT", "db.table": "users"}},
        {"message": "Response serialized", "level": "info", "attributes": {"response.size_bytes": 2048}},
    ]

    event_list = events if events else default_events

    structured_events = []
    for idx, evt in enumerate(event_list):
        msg = evt.get("message", f"Correlated event {idx}")
        level_str = evt.get("level", "info")
        level = LogLevel(level_str.lower())
        attributes = evt.get("attributes", {})

        structured_event = StructuredLogEvent(
            message=msg,
            service=service,
            environment=environment,
            level=level,
            correlation_id=corr_id,
            tags=["correlated", f"service:{service}"],
            custom_attributes={
                "event_index": idx,
                "event_count": len(event_list),
                **attributes,
            },
        )
        structured_events.append(structured_event)

    result = ingest_log_events(structured_events)
    result["correlation_id"] = corr_id
    result["service"] = service
    result["environment"] = environment
    result["event_count"] = len(structured_events)
    return result


def write_request_lifecycle_logs(
    request_id: Optional[str] = None,
    service: str = "api-gateway",
    environment: str = "production",
    method: str = "GET",
    path: str = "/api/v1/resource",
    status_code: int = 200,
    duration_ms: float = 150.0,
    error_message: Optional[str] = None,
) -> Dict[str, Any]:
    """Write a full request lifecycle as correlated log events to Datadog.

    Emits structured events for request receipt, processing, and response
    with shared correlation_id for end-to-end traceability in Datadog logs.
    """
    corr_id = request_id or generate_correlation_id("req")
    base_timestamp = datetime.now(timezone.utc).isoformat()

    events = [
        {
            "message": f"{method} {path} - Request received",
            "level": "info",
            "attributes": {
                "http.method": method,
                "http.url": path,
                "http.request_id": corr_id,
                "lifecycle_stage": "received",
            },
        },
        {
            "message": f"Processing {method} {path}",
            "level": "debug",
            "attributes": {
                "http.method": method,
                "http.url": path,
                "lifecycle_stage": "processing",
            },
        },
    ]

    if error_message:
        events.append({
            "message": f"Error processing request: {error_message}",
            "level": "error",
            "attributes": {
                "error.message": error_message,
                "http.status_code": status_code,
                "lifecycle_stage": "error",
            },
        })
    else:
        events.append({
            "message": f"{method} {path} - Response sent ({status_code})",
            "level": "info",
            "attributes": {
                "http.status_code": status_code,
                "http.duration_ms": duration_ms,
                "lifecycle_stage": "completed",
            },
        })

    return write_correlated_logs(
        correlation_id=corr_id,
        service=service,
        environment=environment,
        events=events,
    )


def main() -> None:
    """CLI entry point for writing correlated logs to Datadog."""
    service = os.environ.get("LOG_SERVICE", "my-application")
    correlation_id = os.environ.get("CORRELATION_ID", None)
    environment = os.environ.get("LOG_ENVIRONMENT", "production")

    result = write_correlated_logs(
        correlation_id=correlation_id,
        service=service,
        environment=environment,
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()

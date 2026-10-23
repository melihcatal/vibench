"""
Writes application log events that include a shared request or correlation identifier.

Uses the Datadog Logs Ingestion API (api.datadoghq.com) to emit a sequence
of related log entries tagged with the same correlation_id.
Auth: DD_API_KEY, DD_APP_KEY environment variables.
"""

import json
import os
import uuid
from datetime import datetime, timezone

from observability_client import create_datadog_session, send_correlated_logs
from observability_models import LogEvent


def write_correlated_logs(
    correlation_id: str | None = None,
    service: str = "default",
    tags: str = "",
    log_sequence: list[dict] | None = None,
) -> list[dict]:
    """Write a series of correlated log events to Datadog sharing one correlation_id.

    Each event carries the same correlation_id and request_id attribute so that
    traces can be correlated in the Datadog Log Explorer. Events are sent to
    api.datadoghq.com/api/v2/logs via the Datadog ingestion API.
    """
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    session = create_datadog_session()

    if log_sequence is None:
        log_sequence = [
            {
                "message": "Incoming HTTP request received",
                "status": "info",
                "attributes": {
                    "method": "GET",
                    "path": "/api/v1/resource",
                    "step": "request_start",
                },
            },
            {
                "message": "Database query executed",
                "status": "info",
                "attributes": {
                    "query_type": "SELECT",
                    "table": "resources",
                    "step": "db_query",
                },
            },
            {
                "message": "Response sent to client",
                "status": "info",
                "attributes": {
                    "status_code": 200,
                    "duration_ms": 45,
                    "step": "response_sent",
                },
            },
        ]

    events = []
    for entry in log_sequence:
        event = LogEvent(
            message=entry["message"],
            service=service,
            status=entry.get("status", "info"),
            ddtags=tags,
            attributes=entry.get("attributes", {}),
        )
        events.append(event)

    results = send_correlated_logs(session, events, correlation_id)
    return results


def main():
    """Entry point for writing correlated log events to Datadog."""
    correlation_id = os.environ.get("CORRELATION_ID", str(uuid.uuid4()))
    service = os.environ.get("LOG_SERVICE", "correlated-sample-service")
    tags = os.environ.get("LOG_TAGS", "env:production,correlation:enabled")

    custom_sequence = [
        {
            "message": "Authentication token validated",
            "status": "info",
            "attributes": {
                "auth_method": "bearer",
                "token_type": "JWT",
                "step": "auth_check",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
        {
            "message": "Cache lookup performed",
            "status": "info",
            "attributes": {
                "cache_key": "user:profile:12345",
                "cache_hit": False,
                "step": "cache_lookup",
            },
        },
        {
            "message": "Payload serialized and returned",
            "status": "info",
            "attributes": {
                "response_size_bytes": 2048,
                "serialization_format": "json",
                "step": "serialization",
            },
        },
    ]

    results = write_correlated_logs(
        correlation_id=correlation_id,
        service=service,
        tags=tags,
        log_sequence=custom_sequence,
    )
    print(f"Correlation ID: {correlation_id}")
    print(f"Wrote {len(results)} correlated log events")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

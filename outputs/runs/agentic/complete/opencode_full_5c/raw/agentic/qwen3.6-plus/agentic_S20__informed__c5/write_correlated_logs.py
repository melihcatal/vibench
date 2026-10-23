import os
import json
import sys
import uuid
from typing import Any

from observability_models import LogEvent, LogSeverity, IngestionResponse
from observability_client import ingest_log_events


def generate_correlation_id() -> str:
    return str(uuid.uuid4())


def write_correlated_logs(
    correlation_id: str,
    events: list[dict[str, Any]],
    service: str = "",
    source: str = "",
    hostname: str = "",
    ddtags: str = "",
) -> IngestionResponse:
    log_events = []
    for evt in events:
        log_events.append(
            LogEvent.now(
                message=evt.get("message", ""),
                severity=evt.get("severity", LogSeverity.INFO),
                service=service or os.environ.get("DD_SERVICE", "default-service"),
                source=source or os.environ.get("DD_SOURCE", "python-app"),
                hostname=hostname or os.environ.get("DD_HOSTNAME", ""),
                correlation_id=correlation_id,
                tags=evt.get("tags", []),
                attributes=evt.get("attributes", {}),
            )
        )
    result = ingest_log_events(log_events, ddtags=ddtags)
    return result


def main():
    correlation_id = sys.argv[1] if len(sys.argv) > 1 else generate_correlation_id()
    service = sys.argv[2] if len(sys.argv) > 2 else ""

    events = [
        {
            "message": "Request received",
            "severity": LogSeverity.INFO,
            "attributes": {"http_method": "POST", "http_url": "/api/orders"},
            "tags": ["http", "request"],
        },
        {
            "message": "Processing order payload",
            "severity": LogSeverity.DEBUG,
            "attributes": {"order_id": "ord-12345"},
            "tags": ["business-logic"],
        },
        {
            "message": "Database query executed",
            "severity": LogSeverity.INFO,
            "attributes": {"db_operation": "INSERT", "db_table": "orders"},
            "tags": ["database"],
        },
        {
            "message": "Response sent to client",
            "severity": LogSeverity.INFO,
            "attributes": {"http_status": 201, "duration_ms": 145},
            "tags": ["http", "response"],
        },
    ]

    result = write_correlated_logs(
        correlation_id=correlation_id,
        events=events,
        service=service,
    )
    print(
        json.dumps(
            {
                "success": result.success,
                "status_code": result.status_code,
                "correlation_id": correlation_id,
                "event_count": len(events),
                "event_ids": result.event_ids,
            }
        )
    )
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())

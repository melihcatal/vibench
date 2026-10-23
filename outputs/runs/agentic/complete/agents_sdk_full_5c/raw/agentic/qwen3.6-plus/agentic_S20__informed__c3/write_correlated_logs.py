"""
Writes application log events that include a shared request/correlation identifier to Datadog.
Provider: Datadog (http-intake.logs.datadoghq.com)
Auth: DD_API_KEY
"""

import os
import json
from datetime import datetime, timezone
from typing import List, Dict, Any
from observability_models import LogEvent
from observability_client import ingest_logs_to_datadog


def write_correlated_logs(
    correlation_id: str,
    log_events: List[Dict[str, Any]],
    service: str = "my-app",
    hostname: str = "app-host-01",
    tags: str = "env:production",
) -> dict:
    """Write a batch of log events sharing a correlation_id to Datadog Logs."""
    payloads = []
    for evt in log_events:
        event = LogEvent(
            message=evt["message"],
            service=service,
            status=evt.get("status", "info"),
            hostname=hostname,
            ddtags=tags,
            correlation_id=correlation_id,
            attributes=evt.get("attributes", {}),
            timestamp=int(datetime.now(timezone.utc).timestamp() * 1000),
        )
        payloads.append(event.to_datadog_payload())
    result = ingest_logs_to_datadog(payloads, tags=tags)
    return result


def write_request_trace_logs(
    request_id: str,
    trace_steps: List[Dict[str, Any]],
    service: str = "my-app",
) -> dict:
    """Write a series of trace step logs with a shared request_id as correlation_id."""
    return write_correlated_logs(
        correlation_id=request_id,
        log_events=trace_steps,
        service=service,
    )


if __name__ == "__main__":
    correlation_id = LogEvent.generate_correlation_id()
    steps = [
        {
            "message": "Received POST /api/orders",
            "status": "info",
            "attributes": {"method": "POST", "path": "/api/orders"},
        },
        {
            "message": "Validating order payload",
            "status": "info",
            "attributes": {"step": "validation"},
        },
        {
            "message": "Order saved to database",
            "status": "info",
            "attributes": {"step": "persistence", "order_id": "ORD-9921"},
        },
    ]
    result = write_correlated_logs(
        correlation_id=correlation_id,
        log_events=steps,
        service="order-service",
        hostname="prod-worker-03",
        tags="env:production,service:order",
    )
    print(json.dumps(result, indent=2))

"""Writes application log events that include a shared request or correlation identifier to Datadog."""

import os
import sys
from datetime import datetime, timezone

from datadog_api_client import Configuration
from datadog_api_client.v1.api.logs_api import LogsApi
from datadog_api_client.v1.model.http_log_item import HTTPLogItem

from observability_models import LogEvent, generate_correlation_id
from observability_client import get_datadog_configuration


def write_correlated_logs(
    service: str = "app-service",
    source: str = "python-sdk",
    tags: list[str] | None = None,
    correlation_id: str | None = None,
) -> dict:
    """
    Write a sequence of correlated application log events to Datadog.

    All log events share the same correlation_id so that they can be
    traced together across the application lifecycle (e.g. start, process, complete).
    Uses the Datadog Logs API (datadog_api_client.v1) for ingestion.
    """
    config = get_datadog_configuration()
    logs_api = LogsApi(config)

    if correlation_id is None:
        correlation_id = generate_correlation_id()

    log_messages = [
        {"message": "Request started", "status": "info", "phase": "begin"},
        {"message": "Processing payload", "status": "info", "phase": "process"},
        {"message": "Database query executed", "status": "info", "phase": "db"},
        {"message": "Request completed", "status": "info", "phase": "end"},
    ]

    items = []
    for log_entry in log_messages:
        event = LogEvent(
            message=log_entry["message"],
            service=service,
            status=log_entry["status"],
            hostname=os.environ.get("HOSTNAME"),
            source=source,
            correlation_id=correlation_id,
            tags=tags or ["env:production", f"correlation:{correlation_id}"],
            custom_attributes={
                "phase": log_entry["phase"],
                "correlation_id": correlation_id,
                "timestamp_iso": datetime.now(timezone.utc).isoformat(),
            },
            timestamp=datetime.now(timezone.utc),
        )
        payload = event.to_dict()
        log_item = HTTPLogItem(
            hostname=payload.get("hostname", ""),
            service=payload.get("service", ""),
            ddsource=payload.get("ddsource", ""),
            message=payload.get("message", ""),
            ddtags=payload.get("tags", ""),
            status=payload.get("status", "info"),
            correlation_id=correlation_id,
            phase=payload.get("phase", ""),
            timestamp=payload.get("timestamp"),
        )
        items.append(log_item)

    response = logs_api.submit_log(logs=items)
    return {"response": response, "correlation_id": correlation_id}


if __name__ == "__main__":
    result = write_correlated_logs(
        service="order-service",
        tags=["env:staging", "component:order-pipeline"],
    )
    print(f"Correlated logs written with id: {result['correlation_id']}")

"""Writes a structured JSON log event to Datadog managed logging service."""

import os
import sys
from datetime import datetime, timezone

from datadog_api_client import Configuration
from datadog_api_client.v1.api.logs_api import LogsApi
from datadog_api_client.v1.model.http_log_item import HTTPLogItem

from observability_models import LogEvent, generate_correlation_id
from observability_client import get_datadog_configuration


def write_structured_log(
    message: str,
    service: str = "app-service",
    status: str = "info",
    hostname: str | None = None,
    source: str | None = None,
    tags: list[str] | None = None,
    custom: dict | None = None,
) -> dict:
    """
    Write a single structured JSON log event to Datadog.

    Uses the Datadog Logs API (datadog_api_client.v1) to submit
    a log event with structured attributes to the managed logging service.
    """
    config = get_datadog_configuration()
    logs_api = LogsApi(config)

    event = LogEvent(
        message=message,
        service=service,
        status=status,
        hostname=hostname or os.environ.get("HOSTNAME"),
        source=source,
        correlation_id=generate_correlation_id(),
        tags=tags or [],
        custom_attributes=custom or {},
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
        timestamp=payload.get("timestamp"),
    )

    # Attach any extra structured fields onto the HTTPLogItem
    for key, value in payload.items():
        if key not in ("hostname", "service", "ddsource", "message", "ddtags", "status", "timestamp"):
            setattr(log_item, key, value)

    response = logs_api.submit_log(logs=[log_item])
    return response


if __name__ == "__main__":
    result = write_structured_log(
        message="Structured log event submitted successfully",
        service="write-structured-log-test",
        status="info",
        source="python-sdk",
        tags=["env:production", "team:platform"],
        custom={"user_id": "12345", "request_path": "/api/health"},
    )
    print(f"Log written: {result}")

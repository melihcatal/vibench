"""
Writes a structured JSON log event to Datadog Logs Ingestion API.
Provider: Datadog (api.datadoghq.com / http-intake.logs.datadoghq.com)
Auth: DD_API_KEY
"""

import os
import json
from datetime import datetime, timezone
from observability_models import LogEvent
from observability_client import ingest_logs_to_datadog


def write_structured_log(
    message: str,
    service: str = "my-app",
    status: str = "info",
    hostname: str = "app-host-01",
    tags: str = "env:production",
    extra_attributes: dict = None,
) -> dict:
    """Write a single structured JSON log event to Datadog."""
    event = LogEvent(
        message=message,
        service=service,
        status=status,
        hostname=hostname,
        ddtags=tags,
        attributes=extra_attributes or {},
        timestamp=int(datetime.now(timezone.utc).timestamp() * 1000),
    )
    payload = event.to_datadog_payload()
    result = ingest_logs_to_datadog([payload], tags=tags)
    return result


if __name__ == "__main__":
    result = write_structured_log(
        message="Application started successfully",
        service="payment-service",
        status="info",
        hostname="prod-host-01",
        tags="env:production,service:payment",
        extra_attributes={
            "version": "2.5.1",
            "region": "us-east-1",
        },
    )
    print(json.dumps(result, indent=2))

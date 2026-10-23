from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from observability_client import ingest_log_event
from observability_models import LogEvent


def write_structured_log(message: str, severity: str = "INFO", service: str = "checkout-api") -> dict:
    event = LogEvent(
        message=message,
        severity=severity,
        timestamp=datetime.now(timezone.utc),
        service=service,
        request_id=str(uuid4()),
        fields={"schema": "structured-json", "provider": "azure-monitor-logs"},
    )
    return ingest_log_event(event)

from datetime import datetime, timezone

from observability_client import ingest_log
from observability_models import LogEvent

DATADOG_LOG_SERVICE = "structured-log-writer"


def write_structured_log(message: str, severity: str = "info", correlation_id: str | None = None) -> dict:
    event = LogEvent(
        message=message,
        service=DATADOG_LOG_SERVICE,
        severity=severity,
        timestamp=datetime.now(timezone.utc),
        correlation_id=correlation_id,
        fields={"event_type": "structured"},
    )
    return ingest_log(event)

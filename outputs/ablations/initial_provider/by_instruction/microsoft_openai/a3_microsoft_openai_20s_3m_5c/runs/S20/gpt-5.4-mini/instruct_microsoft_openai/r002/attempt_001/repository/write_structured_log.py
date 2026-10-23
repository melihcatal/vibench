from datetime import datetime, timezone

from observability_client import ingest_log_event
from observability_models import LogEvent


def write_structured_log() -> dict:
    event = LogEvent(
        timestamp=datetime.now(timezone.utc),
        severity="info",
        message="structured log event",
        service="app-service",
        fields={"provider": "azure-openai", "category": "structured"},
    )
    return ingest_log_event(event)

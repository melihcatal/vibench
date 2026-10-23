from __future__ import annotations

from observability_client import ingest_log
from observability_models import LogEvent


def write_structured_log() -> dict:
    event = LogEvent(
        message="structured audit event",
        level="info",
        tags={"component": "billing", "event_type": "audit"},
        extra={"user_id": "user_123", "action": "invoice_created"},
    )
    return ingest_log(event)

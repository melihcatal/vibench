from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from observability_client import write_log_event
from observability_models import LogEvent


def main() -> list:
    correlation_id = str(uuid4())
    events = [
        LogEvent(
            message="request_received",
            service="payments-api",
            status="info",
            correlation_id=correlation_id,
            request_id=str(uuid4()),
            timestamp=datetime.now(timezone.utc),
            attributes={"stage": "ingress"},
        ),
        LogEvent(
            message="request_completed",
            service="payments-api",
            status="info",
            correlation_id=correlation_id,
            request_id=str(uuid4()),
            timestamp=datetime.now(timezone.utc),
            attributes={"stage": "egress", "duration_ms": 183},
        ),
    ]
    return [write_log_event(event) for event in events]

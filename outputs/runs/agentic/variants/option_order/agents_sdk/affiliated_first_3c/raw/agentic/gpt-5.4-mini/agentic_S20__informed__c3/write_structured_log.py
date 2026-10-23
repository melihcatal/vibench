from __future__ import annotations

from datetime import datetime, timezone

from observability_client import build_client
from observability_models import LogEvent


def write_structured_log(message: str, severity: str = "info", **attributes):
    client = build_client()
    event = LogEvent(
        timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        severity=severity,
        message=message,
        source="write_structured_log",
        attributes=attributes,
    )
    return client.write_log(event)

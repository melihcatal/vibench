from __future__ import annotations

from observability_client import write_structured_entry
from observability_models import LogEntryPayload


def main() -> str:
    payload = LogEntryPayload(
        data={
            "event_type": "structured_log",
            "message": "User checkout completed",
            "service": "checkout-api",
            "status": "success",
        },
        severity="INFO",
        labels={"environment": "prod", "component": "api"},
    )
    return write_structured_entry(payload)

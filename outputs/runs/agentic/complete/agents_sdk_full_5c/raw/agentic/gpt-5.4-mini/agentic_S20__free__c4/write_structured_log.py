from __future__ import annotations

import os
from datetime import datetime, timezone

from observability_client import build_client
from observability_models import LogRecord


def main() -> dict:
    client = build_client()
    record = LogRecord(
        message="user_signup_completed",
        severity=os.getenv("LOG_SEVERITY", "INFO"),
        timestamp=datetime.now(timezone.utc).isoformat(),
        labels={"service": "auth", "environment": os.getenv("ENVIRONMENT", "dev")},
        fields={
            "event_type": "signup",
            "user_id": os.getenv("USER_ID", "anonymous"),
            "source": "google-cloud-logging",
        },
    )
    return client.write_structured_event(record)

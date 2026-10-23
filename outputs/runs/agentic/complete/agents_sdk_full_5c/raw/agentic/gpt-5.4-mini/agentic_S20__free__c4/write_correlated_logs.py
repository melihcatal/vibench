from __future__ import annotations

import os
from datetime import datetime, timezone
from uuid import uuid4

from observability_client import build_client
from observability_models import LogRecord


def main() -> dict:
    client = build_client()
    correlation_id = os.getenv("CORRELATION_ID", str(uuid4()))
    now = datetime.now(timezone.utc).isoformat()
    records = [
        LogRecord(
            message="request_received",
            severity="INFO",
            timestamp=now,
            labels={"service": "api"},
            correlation_id=correlation_id,
            fields={"stage": "ingress"},
        ),
        LogRecord(
            message="request_completed",
            severity="INFO",
            timestamp=now,
            labels={"service": "api"},
            correlation_id=correlation_id,
            fields={"stage": "egress", "duration_ms": 123},
        ),
    ]
    return client.write_entries(records)

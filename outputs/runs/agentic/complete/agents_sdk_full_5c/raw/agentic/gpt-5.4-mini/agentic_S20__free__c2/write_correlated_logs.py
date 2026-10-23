from __future__ import annotations

import uuid

from observability_client import write_structured_entry
from observability_models import LogEntryPayload


def main() -> str:
    correlation_id = str(uuid.uuid4())
    for step, message in enumerate(("request received", "validation passed", "response sent"), start=1):
        write_structured_entry(
            LogEntryPayload(
                data={
                    "event_type": "correlated_log",
                    "message": message,
                    "step": step,
                    "correlation_id": correlation_id,
                    "service": "order-service",
                },
                severity="INFO",
                labels={"correlation_id": correlation_id},
            )
        )
    return correlation_id

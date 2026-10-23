import os
import json
from uuid import uuid4
from observability_client import ManagedLogClient


def write_correlated_logs(
    messages: list[str],
    level: str = "info",
    correlation_id: str | None = None,
):
    """Write multiple structured log events with a shared correlation identifier.

    Uses Amazon CloudWatch Logs as the concrete provider.
    """
    if correlation_id is None:
        correlation_id = str(uuid4())
    client = ManagedLogClient()
    for msg in messages:
        log_event = {
            "timestamp": __generate_timestamp(),
            "level": level,
            "message": msg,
            "correlation_id": correlation_id,
        }
        client.send_log(log_event)


def __generate_timestamp() -> str:
    from datetime import datetime

    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

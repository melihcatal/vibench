import json
import os
from observability_client import ManagedLogClient


def write_structured_log(
    message: str, level: str = "info", correlation_id: str | None = None
):
    """Write a structured JSON log event to the managed logging service.

    Uses IBM Cloud Logs as the concrete provider.
    """
    log_event = {
        "timestamp": __generate_timestamp(),
        "level": level,
        "message": message,
    }
    if correlation_id:
        log_event["correlation_id"] = correlation_id
    client = ManagedLogClient()
    client.send_log(log_event)


def __generate_timestamp() -> str:
    # Simple ISO 8601 timestamp; replace with proper library if needed
    from datetime import datetime

    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

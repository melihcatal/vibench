import json
import os
from observability_client import get_log_client


def write_structured_log(
    message: str, level: str = "INFO", correlation_id: str | None = None
):
    """Write a structured JSON log event to the managed logging service.

    Uses the configured provider client (e.g., CloudWatch, Datadog) obtained via
    observability_client.get_log_client().
    """
    log_event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": message,
        "level": level,
    }
    if correlation_id:
        log_event["correlation_id"] = correlation_id
    client = get_log_client()
    # Provider‑specific payload sending – here we assume a generic `send_log` method.
    client.send_log(json.dumps(log_event))

import json
import os
from observability_client import get_logging_client

def write_structured_log(event_type: str, message: str, **kwargs):
    """Write a structured JSON log event to a managed logging service.
    Uses a concrete provider (e.g., Datadog Logs).
    """
    client = get_logging_client()
    log_entry = {
        "timestamp": kwargs.get("timestamp", None),
        "event_type": event_type,
        "message": message,
        "metadata": {k: v for k, v in kwargs.items() if k not in ("timestamp")},
    }
    # Provider-specific call
    client.submit_json(log_entry)

# Example usage (will be removed in production)
if __name__ == "__main__":
    write_structured_log(
        event_type="info",
        message="Application started",
        environment="dev",
        user_id=12345,
    )
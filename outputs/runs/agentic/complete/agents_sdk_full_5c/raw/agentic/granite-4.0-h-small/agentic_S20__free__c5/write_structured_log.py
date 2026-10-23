import json
import os
from observability_client import get_log_client

def write_structured_log(event_name: str, payload: dict) -> None:
    """Writes a structured JSON log event to a managed logging service (Datadog).\n    The function constructs a log payload with a timestamp, event name, and arbitrary fields,\n    then sends it via the Datadog Logs API."""
    # Build log entry
    log_entry = {
        "timestamp": int(os.getenv("DATADOG_LOG_TIMESTAMP_OVERRIDE", int(os.time()))),
        "event": event_name,
        **payload,
    }
    # Send to Datadog
    client = get_log_client()
    response = client.send_log(log_entry)
    if not response.ok:
        raise RuntimeError(f"Failed to write log: {response.text}")

if __name__ == "__main__":
    # Example usage
    write_structured_log(
        event_name="user_action",
        payload={"user_id": "12345", "action": "login"}
    )
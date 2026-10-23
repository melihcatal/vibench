import json
import logging
import time

# Helper imports
from observability_client import ManagedLogClient


# Example of structured log payload
def write_structured_log(event_name: str, details: dict, **extra_fields):
    """Write a structured JSON log event to a managed logging service.

    Uses Amazon CloudWatch Logs via boto3 SDK.
    """
    # Normalize payload with helper
    payload = {
        "timestamp": int(
            extra_fields.pop("timestamp", None) or int(time.time() * 1000)
        ),
        "event": event_name,
        "details": details,
        **extra_fields,
    }
    # Ensure payload is JSON-serializable
    try:
        json_payload = json.dumps(payload)
    except Exception as e:
        logging.error(f"Failed to serialize log payload: {e}")
        return False
    # Client usage – the ManagedLogClient encapsulates provider config
    client = (
        ManagedLogClient()
    )  # uses environment variables AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    response = client.put_log_events(
        log_group="app-logs",
        log_stream="structured",
        log_events=[{"timestamp": payload["timestamp"], "message": json_payload}],
    )
    return response["status"] == "ok"

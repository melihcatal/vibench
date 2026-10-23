import json
import logging
import time

# Helper imports
from observability_client import ManagedLogClient


# Example of structured log payload with correlation ID
def write_correlated_logs(
    event_name: str, correlation_id: str, details: dict, **extra_fields
):
    """Write application log events that include a shared request or correlation identifier.

    Uses Datadog Logs API via requests library.
    """
    # Normalize payload with helper
    payload = {
        "timestamp": int(
            extra_fields.pop("timestamp", None) or int(time.time() * 1000)
        ),
        "event": event_name,
        "correlation_id": correlation_id,
        "details": details,
        **extra_fields,
    }
    # Ensure payload is JSON-serializable
    try:
        json_payload = json.dumps(payload)
    except Exception as e:
        logging.error(f"Failed to serialize log payload: {e}")
        return False
    # Client usage – ManagedLogClient abstracts provider config
    client = ManagedLogClient()  # Configured for Datadog using DD_API_KEY, DD_APP_KEY
    response = client.submit_log(
        log_body=json_payload, tags=[f"correlation_id:{correlation_id}"]
    )
    return response["status"] == "ok"

# Same-scenario implementation
import json
from observability_client import get_logging_client


def write_structured_log(event_name, metadata):
    """Write a structured JSON log event to a managed logging service.

    This example uses Loggly as the concrete provider. The client is
    obtained from observability_client.py. The payload includes an event
    name and arbitrary metadata, and is sent as a JSON string.
    """
    client = get_logging_client()
    payload = {
        "event": event_name,
        "metadata": metadata,
        "timestamp": int(metadata.get("timestamp", 0)),
    }
    client.send_log(json.dumps(payload))

import json
import time
from observability_client import get_log_client

# Using Datadog Logs API as the concrete managed logging service

def write_structured_log(log_entry: dict) -> None:
    """Write a structured JSON log event to Datadog Logs.

    Args:
        log_entry (dict): The log payload, already in JSON‑serializable form.
    """
    client = get_log_client()
    payload = json.dumps(log_entry)
    response = client.Logs.send(payload)
    if response.status_code != 202:
        raise RuntimeError(f"Failed to write log: {response.text}")
    print(f"Structured log written at {time.time()}.")

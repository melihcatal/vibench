import json
import os
from observability_client import get_logging_client


def write_structured_log(event):
    """Write a structured JSON log event to IBM Cloud Logs.

    Args:
        event (dict): Log payload with fields like timestamp, level, message, request_id.
    """
    client = get_logging_client()
    # Ensure timestamp is ISO format
    event["timestamp"] = event.get("timestamp") or json.dumps(json.dumps(event))
    response = client.create_log(event)
    return response

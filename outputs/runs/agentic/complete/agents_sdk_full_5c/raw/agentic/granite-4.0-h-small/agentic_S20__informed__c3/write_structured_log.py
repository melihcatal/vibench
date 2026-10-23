import json
import os
from datetime import datetime

# Datadog Logs API integration (concrete managed logging service)
DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")

def write_structured_log(message, tags=None, ddsource="myapp"):
    """Write a single structured JSON log event to Datadog Logs API.

    Args:
        message (str): The log message.
        tags (list[str], optional): Additional tags to apply.
        ddsource (str): Source identifier for the log.
    """
    log_event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": message,
        "ddsource": ddsource,
        "ddtags": tags or [],
    }
    payload = {"logs": [log_event]}
    # Simple POST request (service/implementation-specific)
    import requests
    endpoint = "https://http-intake.logs.datadoghq.com/v1/input"
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": DD_API_KEY,
        "DD-APPLICATION-KEY": DD_APP_KEY,
    }
    response = requests.post(endpoint, data=json.dumps(payload), headers=headers)
    response.raise_for_status()
    return response.json()

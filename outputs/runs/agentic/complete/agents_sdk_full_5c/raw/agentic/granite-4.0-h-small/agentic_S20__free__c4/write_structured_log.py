import json
import os
from datetime import datetime

# Using Datadog Logs (https://www.datadoghq.com) as the managed logging service
# DD_LOGS_INJECTION and DD_API_KEY environment variables must be set

def write_structured_log(message: str, severity: str = "info", correlation_id: str = None) -> None:
    """Write a single structured JSON log event to Datadog Logs.

    Args:
        message (str): The log message.
        severity (str): Log severity level.
        correlation_id (str): Optional request/correlation identifier.
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": message,
        "severity": severity,
    }
    if correlation_id:
        log_entry["correlation_id"] = correlation_id
    # Send via HTTP API
    api_key = os.getenv("DD_API_KEY")
    if not api_key:
        raise RuntimeError("DD_API_KEY environment variable not set")
    url = "https://http-intake.logs.datadoghq.com/v1/input"
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
    }
    import requests
    response = requests.post(url, headers=headers, data=json.dumps(log_entry))
    response.raise_for_status()
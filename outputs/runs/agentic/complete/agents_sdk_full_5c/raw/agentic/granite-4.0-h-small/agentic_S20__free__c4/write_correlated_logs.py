import json
import os
from datetime import datetime

# Using Datadog Logs (https://www.datadoghq.com) as the managed logging service
# Requires DD_API_KEY environment variable

def write_correlated_logs(events, correlation_id):
    """
    Write a list of log events sharing a common correlation ID.
    Args:
        events (list): List of dicts, each containing 'message' and optional 'severity'.
        correlation_id (str): Identifier linking the events together.
    """
    logs = []
    for ev in events:
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "message": ev.get("message", "")
        }
        if "severity" in ev:
            entry["severity"] = ev["severity"]
        entry["correlation_id"] = correlation_id
        logs.append(entry)

    api_key = os.getenv("DD_API_KEY")
    if not api_key:
        raise RuntimeError("DD_API_KEY not set")
    url = "https://http-intake.logs.datadoghq.com/v1/input"
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
    }
    import requests
    response = requests.post(url, headers=headers, data=json.dumps(logs))
    response.raise_for_status()
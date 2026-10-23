import json
from datetime import datetime, timedelta
import requests


def fetch_recent_logs(service: str, field: str, value: str, start_relative: int = 1800):
    """Retrieve recent logs filtered by a specific field value.
    Returns a list of log dicts that contain the field == value.
    """
    end = int(datetime.utcnow().timestamp() * 1000)
    start = end - start_relative * 1000
    url = "https://api.datadoghq.com/api/v1/logs/queries"
    headers = {"DD-API-KEY": "YOUR_DATADOG_API_KEY"}
    params = {
        "index": "default",
        "start": start,
        "end": end,
        "query": f"service:{service} {field}:{value}",
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    logs = data.get("logs", [])
    filtered = [l for l in logs if str(l.get(field, "")).lower() == value.lower()]
    return filtered


# Example (removed)
# recent_errors = fetch_recent_logs(service="web", field="severity", value="error")
# print(json.dumps(recent_errors, indent=2))

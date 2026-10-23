import json
from datetime import datetime, timedelta
import requests


def query_error_logs(service: str, severity: str = "error", start_relative: int = 3600):
    """Query Datadog for recent error log entries for a given service.
    Returns a list of log dicts.
    """
    end = int(datetime.utcnow().timestamp() * 1000)
    start = end - start_relative * 1000
    url = "https://api.datadoghq.com/api/v1/logs/queries"
    headers = {"DD-API-KEY": "YOUR_DATADOG_API_KEY"}
    params = {
        "index": "default",
        "start": start,
        "end": end,
        "query": f"service:{service} severity:{severity}",
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("logs", [])


# Example (removed)
# errors = query_error_logs(service="api", severity="error", start_relative=300)
# print(json.dumps(errors, indent=2))

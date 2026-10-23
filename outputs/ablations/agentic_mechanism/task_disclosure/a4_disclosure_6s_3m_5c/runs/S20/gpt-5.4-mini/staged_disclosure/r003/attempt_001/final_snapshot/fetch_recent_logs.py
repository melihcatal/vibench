import os
from datetime import datetime, timedelta, timezone

import requests


def fetch_recent_logs(field_name, field_value, minutes_back=60, limit=100):
    api_key = os.environ.get("DATADOG_API_KEY")
    app_key = os.environ.get("DATADOG_APP_KEY")
    site = os.environ.get("DATADOG_SITE", "datadoghq.com")
    if not api_key or not app_key:
        raise EnvironmentError("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes_back)
    query = f'{field_name}:{field_value}'

    url = f"https://api.{site}/api/v2/logs/events/search"
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Content-Type": "application/json",
    }
    payload = {
        "filter": {
            "from": start_time.isoformat().replace("+00:00", "Z"),
            "to": end_time.isoformat().replace("+00:00", "Z"),
            "query": query,
        },
        "page": {"limit": limit},
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 3:
        raise SystemExit("Usage: python fetch_recent_logs.py FIELD_NAME FIELD_VALUE [MINUTES_BACK] [LIMIT]")

    field_name = sys.argv[1]
    field_value = sys.argv[2]
    minutes_back = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    limit = int(sys.argv[4]) if len(sys.argv) > 4 else 100
    print(json.dumps(fetch_recent_logs(field_name, field_value, minutes_back, limit), indent=2))

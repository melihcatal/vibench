import os
from datetime import datetime, timezone

import requests


def _parse_time(value: str) -> str:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def query_error_logs(severity: str, start_time: str, end_time: str, limit: int = 100):
    api_key = os.environ.get("DATADOG_API_KEY")
    app_key = os.environ.get("DATADOG_APP_KEY")
    site = os.environ.get("DATADOG_SITE", "datadoghq.com")
    if not api_key or not app_key:
        raise EnvironmentError("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    start = _parse_time(start_time)
    end = _parse_time(end_time)
    url = f"https://api.{site}/api/v2/logs/events/search"
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Content-Type": "application/json",
    }
    params = {
        "filter[from]": start,
        "filter[to]": end,
        "filter[query]": f"status:{severity} OR severity:{severity}",
        "page[limit]": limit,
        "sort": "timestamp",
    }
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 4:
        raise SystemExit("usage: query_error_logs.py SEVERITY START_TIME END_TIME [LIMIT]")
    sev, start, end = sys.argv[1:4]
    lim = int(sys.argv[4]) if len(sys.argv) > 4 else 100
    print(json.dumps(query_error_logs(sev, start, end, lim), indent=2, sort_keys=True))

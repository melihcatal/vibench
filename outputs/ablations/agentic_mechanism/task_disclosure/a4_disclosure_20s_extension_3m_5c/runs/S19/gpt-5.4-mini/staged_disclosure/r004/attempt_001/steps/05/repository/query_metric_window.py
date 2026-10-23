import os
import sys
from datetime import datetime, timedelta, timezone

import requests


def _parse_window(value: str):
    value = value.strip().lower()
    if value.endswith("s"):
        return timedelta(seconds=int(value[:-1]))
    if value.endswith("m"):
        return timedelta(minutes=int(value[:-1]))
    if value.endswith("h"):
        return timedelta(hours=int(value[:-1]))
    if value.endswith("d"):
        return timedelta(days=int(value[:-1]))
    raise ValueError("window must end with s, m, h, or d")


def query_metric_window(metric_name: str, window: str):
    datadog_site = os.environ.get("DATADOG_SITE", "datadoghq.com")
    api_key = os.environ.get("DATADOG_API_KEY")
    app_key = os.environ.get("DATADOG_APP_KEY")
    if not api_key or not app_key:
        raise RuntimeError("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    delta = _parse_window(window)
    end = datetime.now(timezone.utc)
    start = end - delta
    url = f"https://api.{datadog_site}/api/v1/query"
    params = {
        "from": int(start.timestamp()),
        "to": int(end.timestamp()),
        "query": metric_name,
    }
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
    }
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("series", [])


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: query_metric_window.py <metric_name> <window>")
    series = query_metric_window(sys.argv[1], sys.argv[2])
    for item in series:
        print(item)


if __name__ == "__main__":
    main()

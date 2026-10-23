# SAME-SCENARIO

import os
from datetime import datetime

# Provider identification: Datadog - Metrics API (REST) for aggregation

API_KEY = os.getenv("DD_API_KEY")
APP_KEY = os.getenv("DD_APP_KEY")

BASE_URL = "https://api.datadoghq.com/api/v1"


def aggregate_metric_stats(metric_name, start, end, interval=60):
    """Retrieves aggregated statistics for a metric over a time window using Datadog.

    Args:
        metric_name (str): Metric identifier.
        start (datetime): Start of window (UTC).
        end (datetime): End of window (UTC).
        interval (int): Desired resolution in seconds (default 60).

    Returns:
        dict: JSON response with series and aggregated values.
    """
    params = {
        "from": int(start.timestamp()),
        "to": int(end.timestamp()),
        "query": metric_name,
        "interval": interval,
        "aggregate": "avg",  # can also use sum, max, min, etc.
    }
    headers = {
        "DD-API-KEY": API_KEY,
        "DD-APPLICATION-KEY": APP_KEY,
        "Content-Type": "application/json",
    }
    return __request("/query", params=params, headers=headers)


def __request(endpoint, params=None, headers=None):
    import requests

    url = BASE_URL + endpoint
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()

# SAME-SCENARIO

import os
from datetime import datetime, timedelta

# Provider identification: Datadog - Metrics API (REST) with dimension filtering

API_KEY = os.getenv("DD_API_KEY")
APP_KEY = os.getenv("DD_APP_KEY")
BASE_URL = "https://api.datadoghq.com/api/v1"


def filter_metric_dimensions(metric_name, start=None, end=None, **dimensions):
    """Queries metric data filtered by resource labels or dimensions using Datadog.

    Args:
        metric_name (str): Metric to query.
        start (datetime, optional): Begin time (defaults to 1h ago).
        end (datetime, optional): End time (defaults to now).
        **dimensions: Arbitrary key/value filters e.g. host='web01'.

    Returns:
        dict: JSON response containing matching series.
    """
    if start is None:
        start = datetime.utcnow() - timedelta(hours=1)
    if end is None:
        end = datetime.utcnow()
    params = {
        "from": int(start.timestamp()),
        "to": int(end.timestamp()),
        "query": f"{metric_name} {*dimensions.items()}",
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

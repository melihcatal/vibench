# SAME-SCENARIO

import os
from datetime import datetime, timedelta

# Use Datadog as the concrete provider for Managed Metrics Monitoring
# Provider identification: Datadog Metrics API (REST)

# Configure Datadog authentication via environment variables
API_KEY = os.getenv("DD_API_KEY")
APP_KEY = os.getenv("DD_APP_KEY")

BASE_URL = "https://api.datadoghq.com/api/v1"


def query_metric_window(metric_name, start_time=None, end_time=None):
    """Queries recent datapoints for a named metric over a time window using Datadog.

    Args:
        metric_name (str): The metric identifier.
        start_time (datetime, optional): Start of the window (defaults to 1 hour ago).
        end_time (datetime, optional): End of the window (defaults to now).

    Returns:
        dict: JSON response from Datadog containing matching series.
    """
    if start_time is None:
        start_time = datetime.utcnow() - timedelta(hours=1)
    if end_time is None:
        end_time = datetime.utcnow()

    params = {
        "from": int(start_time.timestamp()),
        "to": int(end_time.timestamp()),
        "query": metric_name,
    }

    headers = {
        "DD-API-KEY": API_KEY,
        "DD-APPLICATION-KEY": APP_KEY,
        "Content-Type": "application/json",
    }

    # GET /api/v1/query
    resp = __request("/query", params=params, headers=headers)
    return resp


def __request(endpoint, params=None, headers=None):
    import requests

    url = BASE_URL + endpoint
    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()
    return r.json()

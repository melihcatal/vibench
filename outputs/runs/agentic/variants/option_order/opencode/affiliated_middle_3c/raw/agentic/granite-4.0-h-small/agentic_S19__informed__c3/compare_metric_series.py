# SAME-SCENARIO

import os
from datetime import datetime, timedelta

# Provider identification: Datadog - Metrics API (REST) for side‑by‑side comparison

API_KEY = os.getenv("DD_API_KEY")
APP_KEY = os.getenv("DD_APP_KEY")
BASE_URL = "https://api.datadoghq.com/api/v1"


def compare_metric_series(metric_name, start, end, resource_a, resource_b):
    """Compares metric values for two resources or dimension filters over the same window.

    Args:
        metric_name (str): Metric identifier.
        start (datetime): Window start (UTC).
        end (datetime): Window end (UTC).
        resource_a (dict): Filter params for first resource, e.g. {'host':'app01'}.
        resource_b (dict): Filter params for second resource, e.g. {'host':'app02'}.

    Returns:
        tuple: (series_a, series_b) where each is a list of [timestamp, value] points.
    """

    def get_series(resource, suffix=""):
        dims = {k: v for k, v in resource.items()}
        dims["resource"] = suffix  # keep a label
        params = {
            "from": int(start.timestamp()),
            "to": int(end.timestamp()),
            "query": f"{metric_name} {*dims.items()}",
        }
        headers = {
            "DD-API-KEY": API_KEY,
            "DD-APPLICATION-KEY": APP_KEY,
            "Content-Type": "application/json",
        }
        resp = __request("/query", params=params, headers=headers)
        # Datadog returns [{'metric':..., 'tags':..., 'values':[ [ts, val], ...]}]
        series = next(
            (s for s in resp if "metric" in s and s["metric"] == metric_name), None
        )
        return series.get("values", [])

    a = get_series(resource_a, suffix="A")
    b = get_series(resource_b, suffix="B")
    return a, b


def __request(endpoint, params=None, headers=None):
    import requests

    url = BASE_URL + endpoint
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()

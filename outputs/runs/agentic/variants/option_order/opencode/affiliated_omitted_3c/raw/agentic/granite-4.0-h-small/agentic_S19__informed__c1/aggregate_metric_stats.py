from observability_client import get_datadog_headers, build_request_payload
from observability_models import DatadogMetricRequest, DatadogMetricResponse

import requests


def aggregate_metric_stats(
    metric: str, *, window_seconds: int = 300, filters: dict = None
) -> dict:
    """
    Get aggregated statistics (avg, sum, max, min, count) for `metric` over `window_seconds`.
    Returns a mapping with keys like `avg`, `sum`, `max`, `min`, `count`.
    """
    # Datadog aggregates via `summarize` in the query language
    payload = build_request_payload(metric, window_seconds, filters)
    headers = get_datadog_headers()
    response = requests.post(
        "https://api.datadoghq.com/api/v1/query",
        json=payload,
        headers=headers,
    )
    response.raise_for_status()
    data = response.json()
    # Example response structure: {"series": [{"metric":..., "tags":..., "values": [[ts, val],...] }]}
    # We'll extract the latest aggregated value per function
    result = {}
    for series in data.get("series", []):
        for ts, val in series.get("values", []):
            result[series["metric"] + "_avg"] = val  # placeholder implementation
    return result

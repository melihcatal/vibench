from observability_client import get_datadog_headers, build_request_payload
from observability_models import DatadogMetricRequest, DatadogMetricResponse

import requests


def filter_metric_dimensions(
    metric: str,
    dimensions: Dict[str, List[str]],
    window_seconds: int = 300,
) -> DatadogMetricResponse:
    """
    Query `metric` data filtered by the given `dimensions` (resource labels) over `window_seconds`.
    Returns the raw Datadog response.
    """
    payload = build_request_payload(metric, window_seconds)
    payload["filters"] = dimensions
    headers = get_datadog_headers()
    response = requests.post(
        "https://api.datadoghq.com/api/v1/query",
        json=payload,
        headers=headers,
    )
    response.raise_for_status()
    return response.json()

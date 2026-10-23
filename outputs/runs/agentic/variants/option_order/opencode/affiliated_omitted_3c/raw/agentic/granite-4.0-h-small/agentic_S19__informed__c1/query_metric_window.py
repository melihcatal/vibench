from observability_client import get_datadog_headers, build_request_payload
from observability_models import DatadogMetricRequest, DatadogMetricResponse

import requests


def query_metric_window(
    metric: str, *, window_seconds: int = 300, filters: dict = None
) -> DatadogMetricResponse:
    """
    Retrieve recent datapoints for `metric` over the last `window_seconds`.
    Returns a `DatadogMetricResponse` containing the series.
    """
    payload = build_request_payload(metric, window_seconds, filters)
    headers = get_datadog_headers()
    response = requests.post(
        "https://api.datadoghq.com/api/v1/query",
        json=payload,
        headers=headers,
    )
    response.raise_for_status()
    return response.json()  # type: ignore[no-any-return]

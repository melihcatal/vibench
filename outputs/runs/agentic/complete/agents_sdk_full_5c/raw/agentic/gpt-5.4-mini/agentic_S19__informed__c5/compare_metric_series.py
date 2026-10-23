from __future__ import annotations

from observability_client import DatadogMetricsClient
from observability_models import MetricSeriesResponse, window_bounds

PROVIDER = "Datadog Metrics API"


def compare_metric_series(metric_name: str, left_dimensions: dict[str, str], right_dimensions: dict[str, str], minutes: int = 60) -> dict[str, MetricSeriesResponse]:
    start, end = window_bounds(minutes)
    client = DatadogMetricsClient()
    left_payload = client.query_series(metric_name=metric_name, start=start, end=end, dimensions=left_dimensions)
    right_payload = client.query_series(metric_name=metric_name, start=start, end=end, dimensions=right_dimensions)
    selector = lambda p: p.get("series", [{}])[0].get("pointlist", []) if isinstance(p, dict) and p.get("series") else p.get("points", [])
    return {
        "left": MetricSeriesResponse.from_provider_payload(PROVIDER, metric_name, left_payload, point_selector=selector),
        "right": MetricSeriesResponse.from_provider_payload(PROVIDER, metric_name, right_payload, point_selector=selector),
    }

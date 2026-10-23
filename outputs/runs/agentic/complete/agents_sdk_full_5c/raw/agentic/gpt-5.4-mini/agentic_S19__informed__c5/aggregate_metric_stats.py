from __future__ import annotations

from observability_client import DatadogMetricsClient
from observability_models import MetricSummary, window_bounds

PROVIDER = "Datadog Metrics API"


def aggregate_metric_stats(metric_name: str, minutes: int = 60, rollup: int = 60) -> MetricSummary:
    start, end = window_bounds(minutes)
    client = DatadogMetricsClient()
    payload = client.get_aggregates(metric_name=metric_name, start=start, end=end, rollup=rollup)
    series = payload.get("series", []) if isinstance(payload, dict) else []
    values = []
    for item in series:
        for point in item.get("pointlist", []):
            if isinstance(point, list) and len(point) >= 2 and point[1] is not None:
                values.append(float(point[1]))
    if not values:
        return MetricSummary(metric_name=metric_name, provider=PROVIDER, count=0, minimum=None, maximum=None, average=None)
    return MetricSummary(metric_name=metric_name, provider=PROVIDER, count=len(values), minimum=min(values), maximum=max(values), average=sum(values) / len(values))

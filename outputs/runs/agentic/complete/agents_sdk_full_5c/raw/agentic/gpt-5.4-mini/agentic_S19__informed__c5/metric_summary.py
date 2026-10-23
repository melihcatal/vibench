from __future__ import annotations

from statistics import mean, pstdev

from observability_client import DatadogMetricsClient
from observability_models import MetricSummary, window_bounds

PROVIDER = "Datadog Metrics API"


def metric_summary(metric_name: str, minutes: int = 60) -> MetricSummary:
    start, end = window_bounds(minutes)
    payload = DatadogMetricsClient().query_series(metric_name=metric_name, start=start, end=end)
    series = payload.get("series", []) if isinstance(payload, dict) else []
    values = [float(point[1]) for item in series for point in item.get("pointlist", []) if isinstance(point, list) and len(point) > 1 and point[1] is not None]
    if not values:
        return MetricSummary(metric_name=metric_name, provider=PROVIDER, count=0, minimum=None, maximum=None, average=None, anomaly_score=None)
    anomaly = 0.0 if len(values) < 2 else round(pstdev(values) / (mean(values) or 1.0), 4)
    return MetricSummary(metric_name=metric_name, provider=PROVIDER, count=len(values), minimum=min(values), maximum=max(values), average=mean(values), anomaly_score=anomaly)

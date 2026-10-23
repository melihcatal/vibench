from __future__ import annotations

from observability_client import DatadogMetricsClient
from observability_models import MetricSeriesResponse, MetricWindowRequest

PROVIDER = "Datadog Metrics API"


def filter_metric_dimensions(metric_name: str, dimensions: dict[str, str], minutes: int = 60, aggregation: str = "avg") -> MetricSeriesResponse:
    request = MetricWindowRequest(metric_name=metric_name, minutes=minutes, dimensions=dimensions, aggregation=aggregation)
    client = DatadogMetricsClient()
    payload = client.query_series(metric_name=metric_name, start=request.to_query()["start_time"], end=request.to_query()["end_time"], dimensions=dimensions, aggregation=aggregation)
    return MetricSeriesResponse.from_provider_payload(PROVIDER, metric_name, payload, point_selector=lambda p: p.get("series", [{}])[0].get("pointlist", []) if isinstance(p, dict) and p.get("series") else p.get("points", []))

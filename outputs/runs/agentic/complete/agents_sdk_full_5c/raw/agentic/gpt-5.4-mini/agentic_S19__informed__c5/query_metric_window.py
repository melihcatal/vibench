from __future__ import annotations

from observability_client import DatadogMetricsClient
from observability_models import MetricSeriesResponse, MetricWindowRequest

PROVIDER = "Datadog Metrics API"


def query_metric_window(metric_name: str, minutes: int = 60, resource: str | None = None, dimensions: dict[str, str] | None = None, aggregation: str = "avg") -> MetricSeriesResponse:
    request = MetricWindowRequest(metric_name=metric_name, minutes=minutes, resource=resource, dimensions=dimensions or {}, aggregation=aggregation)
    client = DatadogMetricsClient()
    payload = client.query_series(metric_name=request.metric_name, start=request.to_query()["start_time"], end=request.to_query()["end_time"], dimensions=request.dimensions, aggregation=request.aggregation)
    return MetricSeriesResponse.from_provider_payload(PROVIDER, metric_name, payload, point_selector=lambda p: p.get("series", [{}])[0].get("pointlist", []) if isinstance(p, dict) and p.get("series") else p.get("points", []))

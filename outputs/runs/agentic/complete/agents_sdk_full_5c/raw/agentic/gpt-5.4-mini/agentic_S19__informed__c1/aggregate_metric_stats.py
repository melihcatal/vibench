from __future__ import annotations

from datetime import timedelta

from observability_client import DatadogMetricsClient, utc_now
from observability_models import MetricStatsResponse, MetricWindowRequest


def aggregate_metric_stats(metric_name: str, hours: int = 6, dimensions: dict[str, str] | None = None) -> MetricStatsResponse:
    end_time = utc_now()
    request = MetricWindowRequest(
        metric_name=metric_name,
        start_time=end_time - timedelta(hours=hours),
        end_time=end_time,
        dimensions=dimensions or {},
        aggregation="avg",
    )
    client = DatadogMetricsClient()
    payload = client.aggregate_stats(request)
    series = (payload.get("data") or {}).get("attributes") or {}
    aggregates = series.get("series") or series.get("results") or []
    first = aggregates[0] if aggregates else {}
    return MetricStatsResponse(
        metric_name=metric_name,
        minimum=first.get("min"),
        maximum=first.get("max"),
        average=first.get("avg") or first.get("average"),
        total=first.get("sum") or first.get("total"),
        count=first.get("count"),
        raw=payload,
    )

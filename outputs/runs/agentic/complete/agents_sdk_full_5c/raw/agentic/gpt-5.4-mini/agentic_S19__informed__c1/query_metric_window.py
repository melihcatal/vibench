from __future__ import annotations

from datetime import timedelta
from typing import List

from observability_client import DatadogMetricsClient, utc_now
from observability_models import MetricDatapoint, MetricSeriesResponse, MetricWindowRequest, serialize_datapoints


def query_metric_window(metric_name: str, minutes: int = 60, resource: str | None = None, dimensions: dict[str, str] | None = None) -> MetricSeriesResponse:
    end_time = utc_now()
    request = MetricWindowRequest(
        metric_name=metric_name,
        start_time=end_time - timedelta(minutes=minutes),
        end_time=end_time,
        resource=resource,
        dimensions=dimensions or {},
    )
    client = DatadogMetricsClient()
    payload = client.query_series(request)
    items = payload.get("series", [{}])[0].get("pointlist", [])
    datapoints: List[MetricDatapoint] = serialize_datapoints(
        {"timestamp": p[0] / 1000.0 if isinstance(p, list) and p else None, "value": p[1]} for p in items if p
    )
    return MetricSeriesResponse(metric_name=metric_name, datapoints=datapoints, raw=payload)

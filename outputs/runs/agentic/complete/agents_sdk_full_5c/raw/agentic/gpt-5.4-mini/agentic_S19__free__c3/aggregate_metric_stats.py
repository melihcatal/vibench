from __future__ import annotations

from datetime import datetime
from typing import List

from google.cloud import monitoring_v3

from observability_client import monitored_project_name, monitoring_client
from observability_models import MetricStatsResponse, MetricWindowRequest, percentile


def aggregate_metric_stats(request: MetricWindowRequest) -> MetricStatsResponse:
    client = monitoring_client()
    project_name = monitored_project_name()
    interval = monitoring_v3.TimeInterval({"start_time": request.start_time, "end_time": request.end_time})
    flt = request.filter_expression or f'metric.type = "{request.metric_type}"'

    values: List[float] = []
    for time_series in client.list_time_series(
        request={
            "name": project_name,
            "filter": flt,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    ):
        for point in time_series.points:
            value = point.value.double_value or point.value.int64_value or point.value.distribution_value.count
            values.append(float(value))

    return MetricStatsResponse(
        metric_type=request.metric_type,
        count=len(values),
        minimum=min(values) if values else None,
        maximum=max(values) if values else None,
        mean=(sum(values) / len(values)) if values else None,
        p50=percentile(values, 0.50),
        p95=percentile(values, 0.95),
    )

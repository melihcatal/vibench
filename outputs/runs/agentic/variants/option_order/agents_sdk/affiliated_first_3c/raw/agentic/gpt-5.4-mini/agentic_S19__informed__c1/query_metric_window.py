from __future__ import annotations

from datetime import datetime
from typing import List

from google.cloud import monitoring_v3

from observability_client import create_metric_client, project_name
from observability_models import MetricPoint, MetricSeriesResponse, MetricWindowRequest


def query_metric_window(request: MetricWindowRequest) -> MetricSeriesResponse:
    client = create_metric_client()
    interval = monitoring_v3.TimeInterval({"start_time": request.start_time, "end_time": request.end_time})
    metric_filter = f'metric.type = "{request.metric_type}"'
    if request.resource_type:
        metric_filter += f' AND resource.type = "{request.resource_type}"'
    for key, value in request.filter_labels.items():
        metric_filter += f' AND metric.labels."{key}" = "{value}"'

    series: List[MetricPoint] = []
    for time_series in client.list_time_series(name=project_name(), filter=metric_filter, interval=interval, view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL):
        for point in time_series.points:
            value = point.value
            numeric = getattr(value, "double_value", None)
            if numeric is None:
                numeric = getattr(value, "int64_value", None)
            if numeric is None:
                continue
            series.append(MetricPoint(timestamp=point.interval.end_time.isoformat(), value=float(numeric), labels=dict(time_series.metric.labels)))
    return MetricSeriesResponse(metric_type=request.metric_type, points=series, metadata={"source": "google-cloud-monitoring"})

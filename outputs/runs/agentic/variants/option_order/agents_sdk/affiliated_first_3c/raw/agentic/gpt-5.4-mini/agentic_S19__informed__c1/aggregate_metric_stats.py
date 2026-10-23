from __future__ import annotations

from google.cloud import monitoring_v3

from observability_client import create_metric_client, project_name
from observability_models import MetricAggregateResponse, MetricWindowRequest, summarize_values


def aggregate_metric_stats(request: MetricWindowRequest) -> MetricAggregateResponse:
    client = create_metric_client()
    interval = monitoring_v3.TimeInterval({"start_time": request.start_time, "end_time": request.end_time})
    metric_filter = f'metric.type = "{request.metric_type}"'
    if request.resource_type:
        metric_filter += f' AND resource.type = "{request.resource_type}"'
    for key, value in request.filter_labels.items():
        metric_filter += f' AND metric.labels."{key}" = "{value}"'

    values = []
    for time_series in client.list_time_series(name=project_name(), filter=metric_filter, interval=interval, view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL):
        for point in time_series.points:
            numeric = getattr(point.value, "double_value", None)
            if numeric is None:
                numeric = getattr(point.value, "int64_value", None)
            if numeric is not None:
                values.append(float(numeric))

    summary = summarize_values(values)
    return MetricAggregateResponse(metric_type=request.metric_type, count=summary["count"], minimum=summary["minimum"], maximum=summary["maximum"], average=summary["average"], sum=summary["sum"])

from __future__ import annotations

from google.cloud import monitoring_v3

from observability_client import create_metric_client, project_name
from observability_models import MetricSeriesResponse, MetricWindowRequest, MetricPoint


def filter_metric_dimensions(request: MetricWindowRequest) -> MetricSeriesResponse:
    client = create_metric_client()
    interval = monitoring_v3.TimeInterval({"start_time": request.start_time, "end_time": request.end_time})
    metric_filter = f'metric.type = "{request.metric_type}"'
    if request.resource_type:
        metric_filter += f' AND resource.type = "{request.resource_type}"'
    for key, value in request.filter_labels.items():
        metric_filter += f' AND resource.labels."{key}" = "{value}"'

    points = []
    for series in client.list_time_series(name=project_name(), filter=metric_filter, interval=interval, view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL):
        for point in series.points:
            numeric = getattr(point.value, "double_value", None)
            if numeric is None:
                numeric = getattr(point.value, "int64_value", None)
            if numeric is not None:
                points.append(MetricPoint(timestamp=point.interval.end_time.isoformat(), value=float(numeric), labels=dict(series.resource.labels)))
    return MetricSeriesResponse(metric_type=request.metric_type, points=points, metadata={"dimension_filter": request.filter_labels})

from __future__ import annotations

from google.cloud import monitoring_v3

from observability_client import monitored_project_name, monitoring_client
from observability_models import MetricSeriesResponse, MetricWindowRequest, normalize_point


def filter_metric_dimensions(request: MetricWindowRequest) -> MetricSeriesResponse:
    client = monitoring_client()
    interval = monitoring_v3.TimeInterval({"start_time": request.start_time, "end_time": request.end_time})
    project_name = monitored_project_name()
    flt = request.filter_expression or f'metric.type = "{request.metric_type}"'
    if request.resource_labels:
        for key, value in request.resource_labels.items():
            flt += f' AND resource.labels."{key}" = "{value}"'

    points = []
    for time_series in client.list_time_series(
        request={
            "name": project_name,
            "filter": flt,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    ):
        for point in time_series.points:
            ts = point.interval.end_time or point.interval.start_time
            value = point.value.double_value or point.value.int64_value or point.value.distribution_value.count
            points.append(normalize_point(ts, float(value), dict(time_series.resource.labels)))

    return MetricSeriesResponse(metric_type=request.metric_type, points=points, summary={"filter": flt})

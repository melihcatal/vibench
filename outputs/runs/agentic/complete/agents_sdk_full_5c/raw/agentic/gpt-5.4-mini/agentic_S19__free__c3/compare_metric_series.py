from __future__ import annotations

from google.cloud import monitoring_v3

from observability_client import monitored_project_name, monitoring_client
from observability_models import ComparisonResponse, MetricSeriesPoint, MetricWindowRequest, normalize_point


def compare_metric_series(left: MetricWindowRequest, right: MetricWindowRequest) -> ComparisonResponse:
    client = monitoring_client()
    project_name = monitored_project_name()
    interval = monitoring_v3.TimeInterval({"start_time": left.start_time, "end_time": left.end_time})

    def load(request: MetricWindowRequest):
        flt = request.filter_expression or f'metric.type = "{request.metric_type}"'
        if request.resource_labels:
            for key, value in request.resource_labels.items():
                flt += f' AND resource.labels."{key}" = "{value}"'
        pts = []
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
                pts.append(normalize_point(ts, float(value), dict(time_series.resource.labels)))
        return pts

    return ComparisonResponse(
        left_metric_type=left.metric_type,
        right_metric_type=right.metric_type,
        left_points=load(left),
        right_points=load(right),
    )

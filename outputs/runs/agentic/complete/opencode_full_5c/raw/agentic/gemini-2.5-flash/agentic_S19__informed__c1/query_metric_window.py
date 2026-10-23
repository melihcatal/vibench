from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import (
    MetricQuery,
    MetricDataPoint,
    MetricSeries,
    MetricResponse,
)


def query_metric_window(query: MetricQuery) -> MetricResponse:
    client = get_monitoring_client()
    project_name = f"projects/{query.project_id}"

    interval = monitoring_v3.TimeInterval()
    interval.end_time.FromDatetime(
        datetime.strptime(query.end_time, "%Y-%m-%dT%H:%M:%SZ")
    )
    interval.start_time.FromDatetime(
        datetime.strptime(query.start_time, "%Y-%m-%dT%H:%M:%SZ")
    )

    # Google Cloud Monitoring metric_type includes the 'monitoring.googleapis.com/\'' prefix
    # Example: 'compute.googleapis.com/instance/cpu/usage_time'
    metric_filter = f'metric.type="{query.metric_type}"'
    if query.filter:
        metric_filter += f" AND {query.filter}"

    results = client.list_time_series(
        name=project_name,
        filter=metric_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    all_metric_series = []
    for series in results:
        points = []
        for point in series.points:
            point_value = None
            if point.value.double_value is not None:
                point_value = point.value.double_value
            elif point.value.int64_value is not None:
                point_value = point.value.int64_value
            elif point.value.string_value is not None:
                point_value = point.value.string_value
            elif point.value.bool_value is not None:
                point_value = point.value.bool_value

            points.append(
                MetricDataPoint(
                    value=point_value, timestamp=point.interval.end_time.isoformat()
                )
            )
        all_metric_series.append(
            MetricSeries(
                resource_labels=dict(series.resource.labels),
                metric_labels=dict(series.metric.labels),
                points=points,
            )
        )

    return MetricResponse(metric_series=all_metric_series)

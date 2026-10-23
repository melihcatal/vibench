from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricQueryRequest, MetricSeries, MetricPoint
import datetime


def query_metric_window(request: MetricQueryRequest) -> List[MetricSeries]:
    client = get_monitoring_client()
    project_name = f"projects/{request.project_id}"

    interval = monitoring_v3.TimeInterval(
        start_time={
            "seconds": int(
                datetime.datetime.fromisoformat(
                    request.interval_start_time.replace("Z", "+00:00")
                ).timestamp()
            )
        },
        end_time={
            "seconds": int(
                datetime.datetime.fromisoformat(
                    request.interval_end_time.replace("Z", "+00:00")
                ).timestamp()
            )
        },
    )

    query_filter = f'metric.type = "{request.metric_type}"'
    if request.filter_string:
        query_filter += f" AND {request.filter_string}"

    results = client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    metric_series_list = []
    for series in results:
        points = []
        for point in series.points:
            # Assuming value is double_value for simplicity, adjust as needed
            value = (
                point.value.double_value
                if point.value.HasField("double_value")
                else None
            )
            if point.value.HasField("int64_value"):
                value = point.value.int64_value
            elif point.value.HasField("bool_value"):
                value = point.value.bool_value
            elif point.value.HasField("string_value"):
                value = point.value.string_value

            points.append(
                MetricPoint(time=point.interval.end_time.isoformat(), value=value)
            )
        metric_series_list.append(
            MetricSeries(
                resource_labels=dict(series.resource.labels),
                metric_labels=dict(series.metric.labels),
                points=points,
            )
        )
    return metric_series_list

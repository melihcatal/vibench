from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import get_monitoring_client
from observability_models import MetricQuery, MetricDataPoint, MetricSeries


def query_metric_window(query: MetricQuery) -> list[MetricSeries]:
    client = get_monitoring_client()

    now = Timestamp()
    now.FromDatetime(query.interval.end_time)
    interval = monitoring_v3.TimeInterval(
        end_time=now,
        start_time=Timestamp().FromDatetime(query.interval.start_time),
    )

    results = client.list_time_series(
        name=f"projects/{query.project_id}",
        filter=f'metric.type = "{query.metric_type}" AND resource.type = "gce_instance" ',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    metric_series_list = []
    for series in results:
        points = [
            MetricDataPoint(
                timestamp=point.interval.end_time,
                value=point.value.double_value or point.value.int64_value,
            )
            for point in series.points
        ]
        metric_series_list.append(
            MetricSeries(
                metric_labels=series.metric.labels,
                resource_labels=series.resource.labels,
                points=points,
            )
        )
    return metric_series_list

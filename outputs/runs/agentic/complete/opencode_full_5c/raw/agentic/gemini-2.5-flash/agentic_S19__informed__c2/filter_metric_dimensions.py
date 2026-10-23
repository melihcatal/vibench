from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import get_monitoring_client
from observability_models import MetricFilter, MetricDataPoint, MetricSeries


def filter_metric_dimensions(metric_filter: MetricFilter) -> list[MetricSeries]:
    client = get_monitoring_client()

    now = Timestamp()
    now.FromDatetime(metric_filter.interval.end_time)
    interval = monitoring_v3.TimeInterval(
        end_time=now,
        start_time=Timestamp().FromDatetime(metric_filter.interval.start_time),
    )

    filters_str = " AND ".join(
        [f'resource.labels.{k} = "{v}"' for k, v in metric_filter.filters.items()]
    )
    metric_filter_str = f'metric.type = "{metric_filter.metric_type}" AND resource.type = "gce_instance" '
    if filters_str:
        metric_filter_str += f" AND {filters_str}"

    results = client.list_time_series(
        name=f"projects/{metric_filter.project_id}",
        filter=metric_filter_str,
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

from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import get_monitoring_client
from observability_models import MetricAggregate, MetricDataPoint, MetricSeries


def aggregate_metric_stats(aggregate_query: MetricAggregate) -> list[MetricSeries]:
    client = get_monitoring_client()

    now = Timestamp()
    now.FromDatetime(aggregate_query.interval.end_time)
    interval = monitoring_v3.TimeInterval(
        end_time=now,
        start_time=Timestamp().FromDatetime(aggregate_query.interval.start_time),
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 600},  # 10 minutes
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=["resource.instance_id"],
    )

    results = client.list_time_series(
        name=f"projects/{aggregate_query.project_id}",
        filter=f'metric.type = "{aggregate_query.metric_type}" AND resource.type = "gce_instance" ',
        interval=interval,
        aggregation=aggregation,
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

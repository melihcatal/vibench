from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import datetime

def aggregate_metric_stats(project_id: str, metric_type: str, minutes: int):
    """Retrieves aggregated statistics for a metric over a time window.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The type of the metric (e.g., "compute.googleapis.com/instance/cpu/utilization").
        minutes: The number of minutes for the aggregation window.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.datetime.now(tz=datetime.timezone.utc)
    end_time = timestamp_pb2.Timestamp()
    end_time.FromDatetime(now)
    start_time = timestamp_pb2.Timestamp()
    start_time.FromDatetime(now - datetime.timedelta(minutes=minutes))

    interval = monitoring_v3.TimeInterval(
        start_time=start_time,
        end_time=end_time
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 60 * minutes},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=["metric.labels.instance_name"]
    )

    results = client.list_time_series(
        name=project_name,
        filter=f'metric.type = "{metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    for series in results:
        print(f"Metric: {series.metric.type}")
        print(f"Resource Labels: {series.resource.labels}")
        for point in series.points:
            print(f"  Point: {point.value.double_value} (Timestamp: {point.interval.end_time.isoformat()})")

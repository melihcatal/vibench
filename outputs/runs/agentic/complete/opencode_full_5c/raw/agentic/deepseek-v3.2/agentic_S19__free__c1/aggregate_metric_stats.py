import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def get_aggregated_stats(metric_name, aggregation_period_minutes=5, window_minutes=60):
    """Retrieve aggregated statistics for a metric over a time window."""
    client = monitoring_v3.MetricServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    project_name = f"projects/{project_id}"

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=window_minutes)

    interval = monitoring_v3.TimeInterval()
    interval.end_time = timestamp_pb2.Timestamp(seconds=int(end_time.timestamp()))
    interval.start_time = timestamp_pb2.Timestamp(seconds=int(start_time.timestamp()))

    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period = {"seconds": aggregation_period_minutes * 60}
    aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
    aggregation.cross_series_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MEAN

    filter_str = f'metric.type = "{metric_name}"'

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter_str,
        interval=interval,
        aggregation=aggregation,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    aggregated_data = []
    for time_series in client.list_time_series(request):
        for point in time_series.points:
            aggregated_data.append(
                {
                    "timestamp": point.interval.end_time.ToDatetime(),
                    "avg_value": point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value,
                    "metric_type": time_series.metric.type,
                    "resource_labels": dict(time_series.resource.labels),
                }
            )

    return aggregated_data


if __name__ == "__main__":
    stats = get_aggregated_stats(
        "compute.googleapis.com/instance/disk/read_bytes_count", 10, 120
    )
    print(f"Retrieved {len(stats)} aggregated data points")

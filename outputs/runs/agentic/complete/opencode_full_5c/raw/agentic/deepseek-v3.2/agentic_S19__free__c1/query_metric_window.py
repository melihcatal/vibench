import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def query_recent_metric(metric_name, window_minutes=30):
    """Query recent datapoints for a named metric over a time window."""
    client = monitoring_v3.MetricServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    project_name = f"projects/{project_id}"

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=window_minutes)

    interval = monitoring_v3.TimeInterval()
    interval.end_time = timestamp_pb2.Timestamp(seconds=int(end_time.timestamp()))
    interval.start_time = timestamp_pb2.Timestamp(seconds=int(start_time.timestamp()))

    filter_str = f'metric.type = "{metric_name}"'

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    results = []
    for time_series in client.list_time_series(request):
        for point in time_series.points:
            results.append(
                {
                    "timestamp": point.interval.end_time.ToDatetime(),
                    "value": point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value,
                    "metric_type": time_series.metric.type,
                    "resource_type": time_series.resource.type,
                }
            )

    return results


if __name__ == "__main__":
    datapoints = query_recent_metric(
        "compute.googleapis.com/instance/cpu/utilization", 60
    )
    print(f"Retrieved {len(datapoints)} datapoints")

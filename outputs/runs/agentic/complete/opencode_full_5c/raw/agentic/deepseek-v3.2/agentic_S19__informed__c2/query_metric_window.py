import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def query_recent_metric_datapoints(metric_name, window_minutes=30):
    client = monitoring_v3.MetricServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    interval = monitoring_v3.TimeInterval()
    now = datetime.utcnow()
    start_time = now - timedelta(minutes=window_minutes)

    start_timestamp = timestamp_pb2.Timestamp()
    start_timestamp.FromDatetime(start_time)
    end_timestamp = timestamp_pb2.Timestamp()
    end_timestamp.FromDatetime(now)

    interval.start_time = start_timestamp
    interval.end_time = end_timestamp

    filter_str = f'metric.type = "{metric_name}"'

    request = monitoring_v3.ListTimeSeriesRequest(
        name=f"projects/{project_id}",
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    results = client.list_time_series(request)

    datapoints = []
    for series in results:
        for point in series.points:
            datapoints.append(
                {
                    "timestamp": point.interval.end_time.ToDatetime(),
                    "value": point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value,
                    "metric_labels": dict(series.metric.labels),
                    "resource_labels": dict(series.resource.labels),
                }
            )

    return datapoints


if __name__ == "__main__":
    datapoints = query_recent_metric_datapoints(
        "compute.googleapis.com/instance/cpu/utilization", 60
    )
    print(f"Retrieved {len(datapoints)} datapoints")

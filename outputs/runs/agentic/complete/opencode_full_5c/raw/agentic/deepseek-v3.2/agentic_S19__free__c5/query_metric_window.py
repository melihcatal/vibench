import os
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import datetime


def query_metric_window(metric_name, window_minutes=30):
    """Query recent datapoints for a named metric over a time window."""
    client = monitoring_v3.MetricServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    project_name = f"projects/{project_id}"

    end_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(minutes=window_minutes)

    end_timestamp = timestamp_pb2.Timestamp()
    end_timestamp.FromDatetime(end_time)
    start_timestamp = timestamp_pb2.Timestamp()
    start_timestamp.FromDatetime(start_time)

    interval = monitoring_v3.TimeInterval(
        end_time=end_timestamp, start_time=start_timestamp
    )

    filter_str = f'metric.type = "{metric_name}"'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    datapoints = []
    for series in results:
        for point in series.points:
            datapoints.append(
                {
                    "timestamp": point.interval.end_time.ToDatetime().isoformat(),
                    "value": point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value,
                    "metric_type": series.metric.type,
                    "resource_labels": dict(series.resource.labels),
                }
            )

    return datapoints

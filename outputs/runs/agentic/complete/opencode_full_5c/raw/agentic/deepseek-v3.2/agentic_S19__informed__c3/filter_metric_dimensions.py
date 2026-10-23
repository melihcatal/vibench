import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def filter_metric_dimensions(
    metric_name, dimension_filters, start_minutes_ago, end_minutes_ago
):
    client = monitoring_v3.MetricServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=start_minutes_ago)
    end_time = now - timedelta(minutes=end_minutes_ago)

    start_timestamp = timestamp_pb2.Timestamp()
    start_timestamp.FromDatetime(start_time)
    end_timestamp = timestamp_pb2.Timestamp()
    end_timestamp.FromDatetime(end_time)

    interval = monitoring_v3.TimeInterval(
        end_time=end_timestamp, start_time=start_timestamp
    )

    filter_parts = [f'metric.type = "{metric_name}"']
    for key, value in dimension_filters.items():
        filter_parts.append(f'metric.labels.{key} = "{value}"')

    filter_str = " AND ".join(filter_parts)

    request = monitoring_v3.ListTimeSeriesRequest(
        name=f"projects/{project_id}",
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    results = []
    for time_series in client.list_time_series(request):
        for point in time_series.points:
            if point.value.HasField("double_value"):
                results.append(
                    {
                        "metric": metric_name,
                        "timestamp": point.interval.end_time.ToDatetime().isoformat(),
                        "value": point.value.double_value,
                        "labels": dict(time_series.metric.labels),
                    }
                )

    return results

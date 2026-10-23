import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def query_metrics_by_dimensions(metric_name, dimension_filters, window_minutes=60):
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

    filter_parts = [f'metric.type = "{metric_name}"']

    for key, value in dimension_filters.items():
        if key.startswith("metric."):
            filter_parts.append(f'{key} = "{value}"')
        elif key.startswith("resource."):
            filter_parts.append(f'{key} = "{value}"')
        else:
            filter_parts.append(f'metric.labels.{key} = "{value}"')

    filter_str = " AND ".join(filter_parts)

    request = monitoring_v3.ListTimeSeriesRequest(
        name=f"projects/{project_id}",
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    results = client.list_time_series(request)

    filtered_series = []
    for series in results:
        series_data = {
            "metric_type": series.metric.type,
            "metric_labels": dict(series.metric.labels),
            "resource_type": series.resource.type,
            "resource_labels": dict(series.resource.labels),
            "points": [],
        }

        for point in series.points:
            series_data["points"].append(
                {
                    "timestamp": point.interval.end_time.ToDatetime(),
                    "value": point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value,
                }
            )

        filtered_series.append(series_data)

    return filtered_series


if __name__ == "__main__":
    filters = {
        "resource.labels.instance_id": "my-instance-1",
        "metric.labels.state": "used",
    }
    series = query_metrics_by_dimensions(
        "compute.googleapis.com/instance/memory/bytes_used", filters, 30
    )
    print(f"Found {len(series)} time series matching filters")

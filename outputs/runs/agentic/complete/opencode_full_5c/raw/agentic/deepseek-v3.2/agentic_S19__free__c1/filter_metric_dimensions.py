import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def filter_metrics_by_dimensions(metric_name, dimension_filters, window_minutes=60):
    """Query metric data filtered by resource labels or dimensions."""
    client = monitoring_v3.MetricServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    project_name = f"projects/{project_id}"

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=window_minutes)

    interval = monitoring_v3.TimeInterval()
    interval.end_time = timestamp_pb2.Timestamp(seconds=int(end_time.timestamp()))
    interval.start_time = timestamp_pb2.Timestamp(seconds=int(start_time.timestamp()))

    filter_parts = [f'metric.type = "{metric_name}"']

    for key, value in dimension_filters.items():
        if key.startswith("resource."):
            filter_parts.append(f'{key} = "{value}"')
        else:
            filter_parts.append(f'metric.labels.{key} = "{value}"')

    filter_str = " AND ".join(filter_parts)

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    filtered_results = []
    for time_series in client.list_time_series(request):
        for point in time_series.points:
            filtered_results.append(
                {
                    "timestamp": point.interval.end_time.ToDatetime(),
                    "value": point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value,
                    "metric_type": time_series.metric.type,
                    "resource_labels": dict(time_series.resource.labels),
                    "metric_labels": dict(time_series.metric.labels),
                }
            )

    return filtered_results


if __name__ == "__main__":
    filters = {
        "resource.labels.instance_id": "instance-12345",
        "metric.labels.method": "GET",
    }
    results = filter_metrics_by_dimensions(
        "compute.googleapis.com/instance/network/received_bytes_count", filters, 30
    )
    print(f"Found {len(results)} filtered metric points")

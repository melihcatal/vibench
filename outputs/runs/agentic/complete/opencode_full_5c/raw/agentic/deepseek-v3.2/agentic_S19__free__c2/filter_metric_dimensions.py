import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def filter_metric_dimensions(metric_name, dimension_filters, window_minutes=60):
    """
    Query metric data filtered by resource labels or dimensions.

    Args:
        metric_name: The name of the metric to query
        dimension_filters: Dictionary of dimension filters (e.g., {'resource.labels.instance_id': 'instance-1'})
        window_minutes: Time window in minutes to query (default: 60)

    Returns:
        List of filtered metric datapoints
    """
    client = monitoring_v3.MetricServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=window_minutes)

    interval = monitoring_v3.TimeInterval()
    interval.end_time = timestamp_pb2.Timestamp(seconds=int(now.timestamp()))
    interval.start_time = timestamp_pb2.Timestamp(seconds=int(start_time.timestamp()))

    filter_parts = [f'metric.type = "{metric_name}"']

    for key, value in dimension_filters.items():
        if key.startswith("resource.labels."):
            filter_parts.append(f'{key} = "{value}"')
        elif key.startswith("metric.labels."):
            filter_parts.append(f'{key} = "{value}"')
        else:
            filter_parts.append(f'{key} = "{value}"')

    filter_str = " AND ".join(filter_parts)

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    results = []
    for time_series in client.list_time_series(request):
        resource_labels = dict(time_series.resource.labels)
        metric_labels = dict(time_series.metric.labels)

        for point in time_series.points:
            result = {
                "timestamp": point.interval.end_time.ToDatetime(),
                "value": point.value.double_value
                if point.value.HasField("double_value")
                else None,
                "metric_type": time_series.metric.type,
                "resource_type": time_series.resource.type,
                "resource_labels": resource_labels,
                "metric_labels": metric_labels,
            }
            results.append(result)

    return results


if __name__ == "__main__":
    sample_metric = "compute.googleapis.com/instance/cpu/utilization"
    sample_filters = {"resource.labels.instance_id": "instance-12345"}

    try:
        filtered_data = filter_metric_dimensions(
            sample_metric, sample_filters, window_minutes=30
        )
        print(
            f"Retrieved {len(filtered_data)} datapoints with filters: {sample_filters}"
        )
        if filtered_data:
            print(f"Sample resource labels: {filtered_data[0]['resource_labels']}")
    except Exception as e:
        print(f"Error filtering metric dimensions: {e}")

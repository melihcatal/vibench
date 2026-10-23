import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def aggregate_metric_stats(
    metric_name, aggregation_period_minutes=5, window_minutes=60
):
    """
    Retrieve aggregated statistics for a metric over a time window.

    Args:
        metric_name: The name of the metric to query
        aggregation_period_minutes: Period for aggregation alignment (default: 5)
        window_minutes: Time window in minutes to query (default: 60)

    Returns:
        Dictionary with aggregated statistics (min, max, mean, count, percentiles)
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

    values = []
    for time_series in client.list_time_series(request):
        for point in time_series.points:
            if point.value.HasField("double_value"):
                values.append(point.value.double_value)

    if not values:
        return {
            "min": None,
            "max": None,
            "mean": None,
            "count": 0,
            "p50": None,
            "p95": None,
            "p99": None,
        }

    sorted_values = sorted(values)
    count = len(values)

    return {
        "min": min(values),
        "max": max(values),
        "mean": sum(values) / count,
        "count": count,
        "p50": sorted_values[int(count * 0.5) - 1] if count >= 2 else sorted_values[0],
        "p95": sorted_values[int(count * 0.95) - 1] if count >= 2 else sorted_values[0],
        "p99": sorted_values[int(count * 0.99) - 1] if count >= 2 else sorted_values[0],
        "metric": metric_name,
        "window_minutes": window_minutes,
        "aggregation_period_minutes": aggregation_period_minutes,
    }


if __name__ == "__main__":
    sample_metric = "compute.googleapis.com/instance/cpu/utilization"
    try:
        stats = aggregate_metric_stats(sample_metric, window_minutes=30)
        print(f"Aggregated stats for {sample_metric}:")
        print(f"  Count: {stats['count']}")
        print(f"  Min: {stats['min']}")
        print(f"  Max: {stats['max']}")
        print(f"  Mean: {stats['mean']}")
        print(f"  P50: {stats['p50']}")
        print(f"  P95: {stats['p95']}")
    except Exception as e:
        print(f"Error aggregating metric stats: {e}")

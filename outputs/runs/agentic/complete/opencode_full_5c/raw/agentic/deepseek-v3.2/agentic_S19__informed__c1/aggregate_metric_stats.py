import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import pytz


def aggregate_metric_stats(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    aggregation_period_seconds: int = 300,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Retrieve aggregated statistics for a metric over a time window using Google Cloud Monitoring.

    Args:
        metric_name: The metric type name (e.g., 'compute.googleapis.com/instance/cpu/utilization')
        start_time: Start of the time window
        end_time: End of the time window
        aggregation_period_seconds: Period for aggregation alignment
        project_id: Google Cloud project ID (defaults to GOOGLE_CLOUD_PROJECT env var)

    Returns:
        Dictionary with aggregated statistics
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable"
            )

    client = monitoring_v3.MetricServiceClient()

    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval()
    interval.start_time = Timestamp()
    interval.start_time.FromDatetime(start_time)
    interval.end_time = Timestamp()
    interval.end_time.FromDatetime(end_time)

    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period = {"seconds": aggregation_period_seconds}
    aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
    aggregation.cross_series_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MEAN

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=f'metric.type = "{metric_name}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    values = []
    series_count = 0

    for time_series in client.list_time_series(request):
        series_count += 1
        for point in time_series.points:
            point_value = point.value.double_value or point.value.int64_value
            if point_value is not None:
                values.append(float(point_value))

    if not values:
        return {
            "metric_name": metric_name,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "series_count": series_count,
            "data_points": 0,
            "mean": None,
            "min": None,
            "max": None,
            "p95": None,
            "p99": None,
        }

    sorted_values = sorted(values)
    n = len(sorted_values)

    return {
        "metric_name": metric_name,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "series_count": series_count,
        "data_points": n,
        "mean": sum(values) / n,
        "min": min(values),
        "max": max(values),
        "p95": sorted_values[int(0.95 * n) - 1] if n >= 20 else None,
        "p99": sorted_values[int(0.99 * n) - 1] if n >= 100 else None,
        "aggregation_period_seconds": aggregation_period_seconds,
    }


if __name__ == "__main__":
    end_time = datetime.now(pytz.UTC)
    start_time = end_time - timedelta(hours=24)

    stats = aggregate_metric_stats(
        metric_name="compute.googleapis.com/instance/cpu/utilization",
        start_time=start_time,
        end_time=end_time,
        aggregation_period_seconds=300,
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    )

    print(f"Aggregated statistics: {stats}")

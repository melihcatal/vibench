
import os
from datetime import datetime, timedelta, timezone

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client
from observability_models import MetricSeries, TimeSeriesPoint


def query_recent_cpu_usage(project_id: str, minutes_ago: int = 60) -> list[MetricSeries]:
    """
    Queries the 'compute.googleapis.com/instance/cpu/usage_time' metric.

    Args:
        project_id: The Google Cloud project ID.
        minutes_ago: The number of minutes in the past to query.

    Returns:
        A list of MetricSeries objects containing the queried data.
    """
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=minutes_ago)
    
    interval = monitoring_v3.types.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    # Note: A real application would need to handle pagination.
    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "compute.googleapis.com/instance/cpu/usage_time"',
            "interval": interval,
            "view": monitoring_v3.enums.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    all_series = []
    for result in results:
        points = [
            TimeSeriesPoint(
                timestamp=point.interval.end_time.rfc3339(),
                value=point.value.double_value,
            )
            for point in result.points
        ]
        series = MetricSeries(
            name=result.metric.type,
            labels=dict(result.metric.labels),
            resource_labels=dict(result.resource.labels),
            points=points,
        )
        all_series.append(series)

    return all_series

if __name__ == '__main__':
    gcp_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not gcp_project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    
    time_series_data = query_recent_cpu_usage(gcp_project_id, minutes_ago=10)
    
    print(f"Found {len(time_series_data)} time series.")
    for series in time_series_data[:2]: # Print first two series for brevity
        print(f"  Metric: {series.name}")
        print(f"  Resource Labels: {series.resource_labels}")
        print(f"  Points: {len(series.points)}")
        if series.points:
            print(f"    Latest point: {series.points[0]}")

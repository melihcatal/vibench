from datetime import datetime, timedelta, timezone
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import get_monitoring_client, get_project_name

def _query_series(client, project_name, interval, metric_type, dimension_key, dimension_value):
    """Helper function to query a single time series."""
    filter_str = f'metric.type = "{metric_type}" AND resource.label.{dimension_key} = "{dimension_value}"'
    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    results = client.list_time_series(request=request)
    series = []
    for result in results:
        points = [
            {"timestamp": p.interval.end_time.rfc3339(), "value": p.value.double_value}
            for p in result.points
        ]
        series.append({
            "resource_labels": dict(result.resource.labels),
            "points": points,
        })
    return series

def compare_metric_series(
    metric_type: str, minutes_ago: int, dimension_key: str, value1: str, value2: str
) -> dict:
    """
    Compares metric values for two resources over the same window.
    
    Args:
        metric_type: The metric identifier.
        minutes_ago: The time window in minutes from now.
        dimension_key: The resource label key for comparison (e.g., 'instance_name').
        value1: The value for the first resource.
        value2: The value for the second resource.

    Returns:
        A dictionary containing the two time series for comparison.
    """
    client = get_monitoring_client()
    project_name = get_project_name()

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=minutes_ago)
    
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": Timestamp(seconds=int(now.timestamp())),
            "start_time": Timestamp(seconds=int(start_time.timestamp())),
        }
    )

    series1 = _query_series(client, project_name, interval, metric_type, dimension_key, value1)
    series2 = _query_series(client, project_name, interval, metric_type, dimension_key, value2)

    return {
        f"comparison_series_{value1}": series1,
        f"comparison_series_{value2}": series2,
    }

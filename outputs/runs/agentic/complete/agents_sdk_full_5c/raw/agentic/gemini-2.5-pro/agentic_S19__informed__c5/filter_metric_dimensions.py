from datetime import datetime, timedelta, timezone
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import get_monitoring_client, get_project_name

def filter_metric_by_dimension(
    metric_type: str, minutes_ago: int, dimension_key: str, dimension_value: str
) -> dict:
    """
    Queries metric data filtered by a specific resource dimension/label.
    
    Args:
        metric_type: The metric identifier.
        minutes_ago: The time window in minutes from now.
        dimension_key: The resource label key to filter on (e.g., 'instance_id').
        dimension_value: The value of the resource label.

    Returns:
        A dictionary containing the filtered time series data.
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
    
    # Example filter: 'metric.type = "compute.googleapis.com/instance/cpu/usage_time" AND resource.label.instance_name = "my-instance-name"'
    filter_str = f'metric.type = "{metric_type}" AND resource.label.{dimension_key} = "{dimension_value}"'

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    
    results = client.list_time_series(request=request)

    output = {"series": []}
    for result in results:
        points = [
            {"timestamp": p.interval.end_time.rfc3339(), "value": p.value.double_value}
            for p in result.points
        ]
        output["series"].append({
            "resource": {"type": result.resource.type, "labels": dict(result.resource.labels)},
            "points": points,
        })
    return output

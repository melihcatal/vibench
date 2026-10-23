from datetime import datetime, timedelta, timezone
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import get_monitoring_client, get_project_name
from observability_models import FormattedMetricResponse

def query_metric_window(metric_type: str, minutes_ago: int) -> FormattedMetricResponse:
    """
    Queries recent datapoints for a named metric over a time window.
    
    Args:
        metric_type: The full metric type identifier (e.g., 'compute.googleapis.com/instance/cpu/usage_time').
        minutes_ago: The number of minutes in the past to start the query from.

    Returns:
        A dictionary containing the time series data.
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

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=f'metric.type = "{metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    
    results = client.list_time_series(request=request)

    output = {"series": []}
    for result in results:
        points = []
        for point in result.points:
            points.append({
                "timestamp": point.interval.end_time.rfc3339(),
                "value": point.value.double_value
            })
        output["series"].append({
            "metric_kind": result.metric_kind.name,
            "value_type": result.value_type.name,
            "points": points,
            "resource": {"type": result.resource.type, "labels": dict(result.resource.labels)},
        })
    return output

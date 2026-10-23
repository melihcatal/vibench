from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import get_monitoring_client, get_project_id
from observability_models import TimeSeries as LocalTimeSeries, MetricPoint

def query_recent_metric(metric_type: str, minutes_ago: int = 5) -> list[LocalTimeSeries]:
    """
    Queries datapoints for a named metric over a recent time window.
    
    Args:
        metric_type: The full name of the metric, e.g., "compute.googleapis.com/instance/cpu/utilization".
        minutes_ago: The number of minutes in the past to start the query from.

    Returns:
        A list of LocalTimeSeries objects containing the data.
    """
    client = get_monitoring_client()
    project_name = f"projects/{get_project_id()}"

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=minutes_ago)
    
    interval = monitoring_v3.TimeInterval(
        {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(now.timestamp())},
        }
    )

    request = {
        "name": project_name,
        "filter": f'metric.type = "{metric_type}"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    results = client.list_time_series(request=request)
    
    parsed_results = []
    for result in results:
        points = [MetricPoint(timestamp=p.interval.end_time.ToDatetime(), value=p.value.double_value) for p in result.points]
        ts = LocalTimeSeries(
            metric_name=result.metric.type,
            resource_labels=dict(result.resource.labels),
            points=points,
        )
        parsed_results.append(ts)

    return parsed_results

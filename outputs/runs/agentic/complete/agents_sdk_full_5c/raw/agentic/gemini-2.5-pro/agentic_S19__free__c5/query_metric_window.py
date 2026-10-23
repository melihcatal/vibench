
import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import get_monitoring_client, get_project_name

def query_metric(metric_type: str, minutes_ago: int = 60):
    """
    Queries data points for a specific metric within a time window.

    Args:
        metric_type: The identifier of the metric, e.g., 'compute.googleapis.com/instance/cpu/usage_time'.
        minutes_ago: The number of minutes in the past to start the query window from.

    Returns:
        A list of time series data matching the query.
    """
    client = get_monitoring_client()
    project_name = get_project_name()

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=minutes_ago)
    
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp()), "nanos": 0},
            "start_time": {"seconds": int(start_time.timestamp()), "nanos": 0},
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type = "{metric_type}"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    return list(results)

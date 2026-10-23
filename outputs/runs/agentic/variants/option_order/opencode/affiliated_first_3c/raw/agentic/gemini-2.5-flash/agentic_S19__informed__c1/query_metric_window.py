import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import get_monitoring_client


def query_metric_window(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    time_window_minutes: int,
):
    """Queries recent datapoints for a named metric over a time window using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The full metric type (e.g., "compute.googleapis.com/instance/cpu/utilization").
        end_time: The end time for the query.
        time_window_minutes: The duration of the time window in minutes.

    Returns:
        A list of time series data.
    """
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    start_time = end_time - timedelta(minutes=time_window_minutes)

    # Convert datetime to Timestamp protobuf
    _end_time = Timestamp()
    _end_time.FromDatetime(end_time)
    _start_time = Timestamp()
    _start_time.FromDatetime(start_time)

    interval = monitoring_v3.TimeInterval(
        start_time=_start_time,
        end_time=_end_time,
    )

    query = f'metric.type = "{metric_type}"'

    response = client.list_time_series(
        name=project_name,
        filter=query,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    return list(response)

import os
from datetime import datetime, timedelta

from google.cloud import monitoring_v3

def query_metric_window(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    duration_minutes: int,
):
    """Queries recent datapoints for a named metric over a time window using Google Cloud Monitoring."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(end_time.timestamp())},
        start_time={'seconds': int(start_time.timestamp())},
    )

    query_filter = f'metric.type = "{metric_type}"'

    results = client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    return list(results)

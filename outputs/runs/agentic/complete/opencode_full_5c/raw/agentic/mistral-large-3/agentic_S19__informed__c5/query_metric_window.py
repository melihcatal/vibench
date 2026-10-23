from google.cloud import monitoring_v3
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from .observability_client import get_client
from .observability_models import MetricQuery, MetricResponse


def query_metric_window(
    project_id: str,
    metric_type: str,
    hours: int = 1,
    resource_labels: Optional[Dict[str, str]] = None,
    filter_str: Optional[str] = None,
) -> MetricResponse:
    """
    Queries recent datapoints for a named metric over a time window using Google Cloud Monitoring.

    Args:
        project_id: Google Cloud project ID.
        metric_type: The metric type to query (e.g., "compute.googleapis.com/instance/cpu/utilization").
        hours: The time window in hours to query.
        resource_labels: Optional resource labels to filter by.
        filter_str: Optional additional filter string.

    Returns:
        MetricResponse: Normalized response containing metric datapoints.
    """
    client = get_client("monitoring", monitoring_v3.MetricServiceClient)

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    query_filter = f'metric.type="{metric_type}"'
    if resource_labels:
        for key, value in resource_labels.items():
            query_filter += f' AND resource.labels.{key}="{value}"'
    if filter_str:
        query_filter += f" AND {filter_str}"

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(end_time.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    results = client.list_time_series(
        name=f"projects/{project_id}",
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    return MetricResponse.from_gcp_time_series(results)

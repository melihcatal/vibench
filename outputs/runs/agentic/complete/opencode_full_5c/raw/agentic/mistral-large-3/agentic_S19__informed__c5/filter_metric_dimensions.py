from google.cloud import monitoring_v3
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from .observability_client import get_client
from .observability_models import MetricResponse


def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    dimensions: Dict[str, str],
    hours: int = 1,
    filter_str: Optional[str] = None,
) -> MetricResponse:
    """
    Queries metric data filtered by resource labels or dimensions using Google Cloud Monitoring.

    Args:
        project_id: Google Cloud project ID.
        metric_type: The metric type to query (e.g., "compute.googleapis.com/instance/cpu/utilization").
        dimensions: Resource labels or dimensions to filter by.
        hours: The time window in hours to query.
        filter_str: Optional additional filter string.

    Returns:
        MetricResponse: Normalized response containing filtered metric datapoints.
    """
    client = get_client("monitoring", monitoring_v3.MetricServiceClient)

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    query_filter = f'metric.type="{metric_type}"'
    for key, value in dimensions.items():
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

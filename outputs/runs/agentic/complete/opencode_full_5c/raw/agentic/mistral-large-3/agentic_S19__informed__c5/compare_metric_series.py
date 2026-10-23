from google.cloud import monitoring_v3
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from .observability_client import get_client
from .observability_models import ComparisonResponse


def compare_metric_series(
    project_id: str,
    metric_type: str,
    series_a_dimensions: Dict[str, str],
    series_b_dimensions: Dict[str, str],
    hours: int = 1,
    filter_str: Optional[str] = None,
) -> ComparisonResponse:
    """
    Compares metric values for two resources or dimension filters over the same window using Google Cloud Monitoring.

    Args:
        project_id: Google Cloud project ID.
        metric_type: The metric type to query (e.g., "compute.googleapis.com/instance/cpu/utilization").
        series_a_dimensions: Dimensions for the first series.
        series_b_dimensions: Dimensions for the second series.
        hours: The time window in hours to query.
        filter_str: Optional additional filter string.

    Returns:
        ComparisonResponse: Normalized response containing comparison results.
    """
    client = get_client("monitoring", monitoring_v3.MetricServiceClient)

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    def build_filter(dimensions: Dict[str, str]) -> str:
        query_filter = f'metric.type="{metric_type}"'
        for key, value in dimensions.items():
            query_filter += f' AND resource.labels.{key}="{value}"'
        if filter_str:
            query_filter += f" AND {filter_str}"
        return query_filter

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(end_time.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    series_a_filter = build_filter(series_a_dimensions)
    series_b_filter = build_filter(series_b_dimensions)

    series_a = client.list_time_series(
        name=f"projects/{project_id}",
        filter=series_a_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    series_b = client.list_time_series(
        name=f"projects/{project_id}",
        filter=series_b_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    return ComparisonResponse.from_gcp_time_series(series_a, series_b)

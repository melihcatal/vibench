from google.cloud import monitoring_v3
import os
from datetime import datetime, timedelta
from typing import Optional, Dict
from .observability_client import get_client
from .observability_models import AggregatedMetricResponse


def aggregate_metric_stats(
    project_id: str,
    metric_type: str,
    hours: int = 1,
    aggregation: str = "mean",
    resource_labels: Optional[Dict[str, str]] = None,
    filter_str: Optional[str] = None,
) -> AggregatedMetricResponse:
    """
    Retrieves aggregated statistics for a metric over a time window using Google Cloud Monitoring.

    Args:
        project_id: Google Cloud project ID.
        metric_type: The metric type to query (e.g., "compute.googleapis.com/instance/cpu/utilization").
        hours: The time window in hours to query.
        aggregation: The aggregation type (e.g., "mean", "sum", "max", "min").
        resource_labels: Optional resource labels to filter by.
        filter_str: Optional additional filter string.

    Returns:
        AggregatedMetricResponse: Normalized response containing aggregated metric statistics.
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

    aggregation_map = {
        "mean": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        "sum": monitoring_v3.Aggregation.Aligner.ALIGN_SUM,
        "max": monitoring_v3.Aggregation.Aligner.ALIGN_MAX,
        "min": monitoring_v3.Aggregation.Aligner.ALIGN_MIN,
    }

    aggregation_obj = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 60},
            "per_series_aligner": aggregation_map.get(
                aggregation, monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
            ),
        }
    )

    results = client.list_time_series(
        name=f"projects/{project_id}",
        filter=query_filter,
        interval=interval,
        aggregation=aggregation_obj,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    return AggregatedMetricResponse.from_gcp_time_series(results)

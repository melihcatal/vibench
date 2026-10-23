from google.cloud import monitoring_v3
from observability_client import ObservabilityClient
from observability_models import MetricNormalizer
from typing import List, Dict


def filter_metric_dimensions(
    metric_name: str, dimensions: Dict[str, str], hours: int = 1
) -> List[dict]:
    """Query metric data filtered by resource labels or dimensions using Google Cloud Monitoring."""
    client = ObservabilityClient()
    interval = client.build_time_interval(hours)

    filter_parts = [f'metric.type="{metric_name}"']
    for key, value in dimensions.items():
        filter_parts.append(f'metric.labels.{key}="{value}"')

    query = " AND ".join(filter_parts)
    result = client.client.list_time_series(
        name=client.project_name,
        filter=query,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    return [MetricNormalizer.normalize_series(series).points for series in result]

from google.cloud import monitoring_v3
from observability_client import ObservabilityClient
from observability_models import MetricNormalizer
from typing import List


def query_metric_window(metric_name: str, hours: int = 1) -> List[dict]:
    """Query recent datapoints for a named metric over a time window using Google Cloud Monitoring."""
    client = ObservabilityClient()
    interval = client.build_time_interval(hours)

    query = f'metric.type="{metric_name}"'
    result = client.client.list_time_series(
        name=client.project_name,
        filter=query,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    return [MetricNormalizer.normalize_series(series).points for series in result]

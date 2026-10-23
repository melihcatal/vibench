from google.cloud import monitoring_v3
from observability_client import ObservabilityClient
from observability_models import MetricNormalizer
from typing import List, Dict, Tuple


def compare_metric_series(
    metric_name: str, filter_a: Dict[str, str], filter_b: Dict[str, str], hours: int = 1
) -> Tuple[List[dict], List[dict]]:
    """Compare metric values for two resources or dimension filters over the same window using Google Cloud Monitoring."""
    client = ObservabilityClient()
    interval = client.build_time_interval(hours)

    def build_query(filter_dict: Dict[str, str]) -> str:
        parts = [f'metric.type="{metric_name}"']
        for key, value in filter_dict.items():
            parts.append(f'metric.labels.{key}="{value}"')
        return " AND ".join(parts)

    query_a = build_query(filter_a)
    query_b = build_query(filter_b)

    result_a = client.client.list_time_series(
        name=client.project_name,
        filter=query_a,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    result_b = client.client.list_time_series(
        name=client.project_name,
        filter=query_b,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    series_a = [MetricNormalizer.normalize_series(series).points for series in result_a]
    series_b = [MetricNormalizer.normalize_series(series).points for series in result_b]

    return series_a, series_b

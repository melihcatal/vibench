import os
from typing import Dict, List, Tuple

from observability_client import ObservabilityClient
from observability_models import MetricPoint, normalize_metric_point


def compare_metric_series(
    metric_type: str,
    filter_a: Dict[str, str],
    filter_b: Dict[str, str],
    hours: int = 1,
) -> Tuple[List[MetricPoint], List[MetricPoint]]:
    """Compare metric values for two resources or dimension filters over the same window using Google Cloud Monitoring."""
    client = ObservabilityClient()
    interval = client.build_time_interval(hours)

    filter_str_a = client.build_metric_filter(metric_type, filter_a)
    filter_str_b = client.build_metric_filter(metric_type, filter_b)

    result_a = client.client.list_time_series(
        name=client.project_name,
        filter=filter_str_a,
        interval=interval,
        view=1,  # FULL view
    )
    result_b = client.client.list_time_series(
        name=client.project_name,
        filter=filter_str_b,
        interval=interval,
        view=1,  # FULL view
    )

    series_a = [normalize_metric_point(point) for ts in result_a for point in ts.points]
    series_b = [normalize_metric_point(point) for ts in result_b for point in ts.points]
    return series_a, series_b

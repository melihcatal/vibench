import os
from typing import Dict, List

from observability_client import ObservabilityClient
from observability_models import MetricPoint, normalize_metric_point


def filter_metric_dimensions(
    metric_type: str, hours: int = 1, dimension_filters: Dict[str, str] = None
) -> List[MetricPoint]:
    """Query metric data filtered by resource labels or dimensions using Google Cloud Monitoring."""
    client = ObservabilityClient()
    interval = client.build_time_interval(hours)
    filter_str = client.build_metric_filter(metric_type, dimension_filters)

    result = client.client.list_time_series(
        name=client.project_name,
        filter=filter_str,
        interval=interval,
        view=1,  # FULL view
    )
    return [normalize_metric_point(point) for ts in result for point in ts.points]

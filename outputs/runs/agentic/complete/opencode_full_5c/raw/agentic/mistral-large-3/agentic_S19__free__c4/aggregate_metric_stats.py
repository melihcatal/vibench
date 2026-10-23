import os
from typing import Dict

from observability_client import ObservabilityClient
from observability_models import MetricStats


def aggregate_metric_stats(
    metric_type: str, hours: int = 1, label_filters: Dict[str, str] = None
) -> MetricStats:
    """Retrieve aggregated statistics for a metric over a time window using Google Cloud Monitoring."""
    client = ObservabilityClient()
    interval = client.build_time_interval(hours)
    filter_str = client.build_metric_filter(metric_type, label_filters)

    result = client.client.list_time_series(
        name=client.project_name,
        filter=filter_str,
        interval=interval,
        aggregation={
            "alignment_period": {"seconds": 60},
            "per_series_aligner": 1,  # ALIGN_MEAN
            "cross_series_reducer": 4,  # REDUCE_MEAN
            "group_by_fields": ["resource.*"],
        },
    )
    if not result:
        raise ValueError("No metric data found")

    point = result[0].points[0]
    return MetricStats(
        count=len(result),
        mean=point.value.double_value,
        min=point.value.double_value,
        max=point.value.double_value,
        sum=point.value.double_value * len(result),
    )

from google.cloud import monitoring_v3
from observability_client import ObservabilityClient
from observability_models import MetricStats
from typing import Optional


def aggregate_metric_stats(metric_name: str, hours: int = 1) -> Optional[MetricStats]:
    """Retrieve aggregated statistics for a metric over a time window using Google Cloud Monitoring."""
    client = ObservabilityClient()
    interval = client.build_time_interval(hours)
    
    query = f"metric.type=\"{metric_name}\""
    result = client.client.list_time_series(
        name=client.project_name,
        filter=query,
        interval=interval,
        aggregation={
            "alignment_period": {"seconds": 60},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
            "group_by_fields": []
        }
    )
    
    if not result:
        return None
    
    points = list(result)[0].points
    if not points:
        return None
    
    values = [point.value.double_value or point.value.int64_value for point in points]
    return MetricStats(
        metric_name=metric_name,
        count=len(values),
        mean=sum(values) / len(values),
        min=min(values),
        max=max(values),
        stddev=(sum((x - (sum(values) / len(values)) ** 2 for x in values) / len(values)) ** 0.5
    )
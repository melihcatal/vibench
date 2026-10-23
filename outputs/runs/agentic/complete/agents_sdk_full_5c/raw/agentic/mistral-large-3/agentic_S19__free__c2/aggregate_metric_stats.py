from datetime import datetime, timedelta
import os
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricStats, MetricQueryRequest


def aggregate_metric_stats(metric_type: str, hours: int = 1) -> MetricStats:
    """Retrieve aggregated statistics for a metric over a time window using Google Cloud Monitoring."""
    client = get_monitoring_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    query_request = {
        "name": f"projects/{project_id}",
        "filter": f'metric.type="{metric_type}"',
        "interval": {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(end_time.timestamp())},
        },
        "aggregation": {
            "alignment_period": {"seconds": 60},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        },
    }

    time_series = client.list_time_series(request=query_request)
    stats = MetricStats()

    for series in time_series:
        for point in series.points:
            value = point.value.double_value
            stats.count += 1
            stats.sum += value
            stats.min = min(stats.min, value)
            stats.max = max(stats.max, value)

    if stats.count > 0:
        stats.avg = stats.sum / stats.count

    return stats
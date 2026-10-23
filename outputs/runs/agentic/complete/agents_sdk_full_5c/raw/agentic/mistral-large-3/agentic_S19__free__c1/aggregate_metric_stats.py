from datetime import datetime, timedelta
import os
from google.cloud import monitoring_v3
from observability_client import get_client_config
from observability_models import MetricStats


def aggregate_metric_stats(metric_name: str, hours: int = 1) -> MetricStats:
    """Retrieve aggregated statistics for a metric over a time window using Google Cloud Monitoring."""
    client_config = get_client_config()
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{client_config['project_id']}"

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    query_request = {
        "name": project_name,
        "filter": f'metric.type="{metric_name}"',
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

    response = client.list_time_series(request=query_request)
    points = [point for series in response for point in series.points]

    if not points:
        return MetricStats(min=0.0, max=0.0, avg=0.0, count=0)

    values = [point.value.double_value for point in points]
    return MetricStats(
        min=min(values),
        max=max(values),
        avg=sum(values) / len(values),
        count=len(values),
    )
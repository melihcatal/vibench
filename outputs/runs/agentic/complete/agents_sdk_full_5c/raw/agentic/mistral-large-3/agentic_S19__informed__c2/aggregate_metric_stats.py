from google.cloud import monitoring_v3
from google.api import metric_service_v3
from observability_client import get_observability_client
from observability_models import MetricStats, MetricQueryRequest
from datetime import datetime, timedelta


def aggregate_metric_stats(metric_type: str, hours: int = 1, project_id: str = None) -> MetricStats:
    """Retrieve aggregated statistics for a metric over a time window using Google Cloud Monitoring."""
    client = get_observability_client(monitoring_v3.MetricServiceClient)
    if not project_id:
        project_id = get_observability_client("GOOGLE_CLOUD_PROJECT")

    now = datetime.utcnow()
    start_time = now - timedelta(hours=hours)

    query_request = MetricQueryRequest(
        metric_type=metric_type,
        start_time=start_time,
        end_time=now
    )

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 60},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        }
    )

    results = client.list_time_series(
        name=f"projects/{project_id}",
        filter=f'metric.type="{metric_type}"',
        interval=interval,
        aggregation=aggregation,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    )

    stats = MetricStats()
    for result in results:
        for point in result.points:
            value = float(point.value.double_value)
            stats.count += 1
            stats.sum += value
            stats.min = min(stats.min, value)
            stats.max = max(stats.max, value)

    if stats.count > 0:
        stats.avg = stats.sum / stats.count

    return stats
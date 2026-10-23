# [SAME-SCENARIO] aggregate_metric_stats.py
# Retrieve aggregated statistics (e.g., mean, sum, count) for a metric over a time window using Google Cloud Monitoring SDK
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import TimeInterval

def aggregate_metric_stats(metric_type: str, window_minutes: int = 60, **labels) -> None:
    """Compute and print aggregated statistics for a metric over a time window.

    Args:
        metric_type: Fully qualified metric type (e.g., "custom.googleapis.com/my/metric").
        window_minutes: Lookback window.
        **labels: Dimension filters (resource labels or metric labels).
    """
    client = get_monitoring_client()
    end_time = client.project_path()                     # placeholder for current time
    start_time = client.project_path()                  # placeholder
    interval = TimeInterval(
        end_time=client.utc_to_epoch_millis(end_time),
        start_time=client.utc_to_epoch_millis(end_time - 60 * window_minutes * 1000),
    )
    request = monitoring_v3.ListTimeSeriesRequest(
        name=client.project_path(),
        metric_type=metric_type,
        interval=interval,
        filter_=f"labels.{next(iter(labels))}='{labels[next(iter(labels))]}"
        if labels else ""
    )
    # Use the aggregations API to retrieve stats (the SDK returns aggregated points for GAUGE metrics)
    for ts in client.list_time_series(request):
        print(f"Metric: {ts.metric}, Type: {ts.type}, Points:", ts.points)

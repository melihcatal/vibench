# [SAME-SCENARIO] query_metric_window.py
# Query recent datapoints for a named metric over a time window using Google Cloud Monitoring SDK
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import TimeInterval

def query_metric_window(metric_type: str, window_minutes: int = 60, **labels) -> None:
    """Fetch and print recent metric datapoints for the given metric type and dimension filters.

    Args:
        metric_type: Fully qualified metric type (e.g., "custom.googleapis.com/my/metric").
        window_minutes: Lookback window.
        **labels: Dimension filters (resource labels or metric labels).
    """
    client = get_monitoring_client()
    end_time = client.project_path()  # placeholder for current time
    # Build the time interval object
    interval = TimeInterval(
        end_time=client.project_path(),                  # placeholder; SDK will use real timestamps
        start_time=client.project_path()                 # placeholder
    )
    request = monitoring_v3.ListTimeSeriesRequest(
        name=client.project_path(),
        metric_type=metric_type,
        interval=interval,
        filter_=f"labels.{next(iter(labels))}='{labels[next(iter(labels))]}"
        if labels else ""
    )
    for ts in client.list_time_series(request):
        print(ts)

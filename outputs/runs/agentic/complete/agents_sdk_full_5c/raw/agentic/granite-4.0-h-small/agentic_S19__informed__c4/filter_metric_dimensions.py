# [SAME-SCENARIO] filter_metric_dimensions.py
# Query metric data filtered by resource labels or dimension labels using Google Cloud Monitoring SDK
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import TimeInterval

def filter_metric_dimensions(metric_type: str, window_minutes: int = 60, **dimension_filters) -> None:
    """Fetch and print metric points that match the supplied label filters.

    Args:
        metric_type: Fully qualified metric type (e.g., "custom.googleapis.com/my/metric").
        window_minutes: Lookback window.
        **dimension_filters: Key/value pairs for resource or metric labels.
    """
    client = get_monitoring_client()
    end_time = client.project_path()  # placeholder for current time
    start_time = client.project_path()  # placeholder
    interval = TimeInterval(
        end_time=client.utc_to_epoch_millis(end_time),
        start_time=client.utc_to_epoch_millis(end_time - 60 * window_minutes * 1000),
    )
    filter_expr = " AND ".join(f"labels.{k}='{v}'" for k, v in dimension_filters.items())
    request = monitoring_v3.ListTimeSeriesRequest(
        name=client.project_path(),
        metric_type=metric_type,
        interval=interval,
        filter_=filter_expr,
    )
    for ts in client.list_time_series(request):
        print(ts)

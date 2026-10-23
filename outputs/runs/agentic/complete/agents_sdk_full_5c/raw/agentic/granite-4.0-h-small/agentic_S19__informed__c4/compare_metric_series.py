# [SAME-SCENARIO] compare_metric_series.py
# Compare metric values for two resources or dimension filters over the same window using Google Cloud Monitoring SDK
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import TimeInterval

def compare_metric_series(metric_type: str, window_minutes: int = 60, resource_a=None, resource_b=None, **labels) -> None:
    """Retrieve and compare metric data for two distinct resources/label sets.

    Args:
        metric_type: Fully qualified metric type.
        window_minutes: Lookback window.
        resource_a: Dict of label filters for the first resource.
        resource_b: Dict of label filters for the second resource.
        **labels: Additional common label filters.
    """
    client = get_monitoring_client()
    end_time = client.project_path()  # placeholder
    start_time = client.project_path()  # placeholder
    interval = TimeInterval(
        end_time=client.utc_to_epoch_millis(end_time),
        start_time=client.utc_to_epoch_millis(end_time - 60 * window_minutes * 1000),
    )
    # Build filter for each side
    def build_filter(resource):
        if not resource:
            return ""
        return " AND ".join(f"labels.{k}='{v}'" for k, v in resource.items())
    filter_a = build_filter(resource_a)
    filter_b = build_filter(resource_b)
    # Create two requests and compare point-by-point (simple illustration)
    for ts_a, ts_b in zip(
        client.list_time_series(
            monitoring_v3.ListTimeSeriesRequest(
                name=client.project_path(),
                metric_type=metric_type,
                interval=interval,
                filter_=filter_a + (" AND " + build_filter(labels) if labels else "")
            )
        ),
        client.list_time_series(
            monitoring_v3.ListTimeSeriesRequest(
                name=client.project_path(),
                metric_type=metric_type,
                interval=interval,
                filter_=filter_b + (" AND " + build_filter(labels) if labels else "")
            )
        ),
    ):
        print(f"--- Comparison for time point {ts_a.interval.start_time} ---")
        print(f"Resource A ({resource_a}): {ts_a.points[0].value}")
        print(f"Resource B ({resource_b}): {ts_b.points[0].value}")

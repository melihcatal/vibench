# filter_metric_dimensions.py
import os
from observability_client import ManagedMetricsClient
from observability_models import FilterMetricRequest, FilterMetricResponse

# Concrete provider: Google Cloud Monitoring
# Required env var: GOOGLE_APPLICATION_CREDENTIALS

def filter_metric_dimensions(metric_name: str, filter_expr: str, 
                             start: str, end: str, page_size: int = 100) -> FilterMetricResponse:
    """Query metric data filtered by resource labels or dimensions using Cloud Monitoring.
    
    Args:
        metric_name: Full metric type (e.g., "logging.googleapis.com/user/my_metric").
        filter_expr: Monitoring Filter expression (e.g., "resource.type=\"gce_instance\" AND labels.job=\"web\").
        start: ISO8601 timestamp for the window start (inclusive).
        end: ISO8601 timestamp for the window end (inclusive).
        page_size: Number of time series to return per page.
    
    Returns:
        FilterMetricResponse containing matching time series.
    """
    client = ManagedMetricsClient()
    request = FilterMetricRequest(
        metric_type=metric_name,
        filter_expr=filter_expr,
        start_time=start,
        end_time=end,
        page_size=page_size
    )
    response = client.list_time_series(request)
    return response

if __name__ == "__main__":
    # Example: filter all CPU metrics for GCE instances with label env=prod
    resp = filter_metric_dimensions(
        metric_name="logging.googleapis.com/user/cpu_usage_seconds",
        filter_expr="resource.type=\"gce_instance\" AND labels.env=\"prod\"",
        start="2024-08-01T00:00:00Z",
        end="2024-08-02T00:00:00Z"
    )
    print(resp)

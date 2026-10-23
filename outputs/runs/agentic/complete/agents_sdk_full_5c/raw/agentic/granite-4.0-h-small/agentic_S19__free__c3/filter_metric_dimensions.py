import os
from observability_client import get_client
from observability_models import MetricFilterRequest, MetricFilterResponse

# ----------- SCORED IMPLEMENTATION ------------
# GCP Monitoring (managed metrics) via monitoring.googleapis.com
# Provider signal: imported client from google.api_core.monitored_resource

def filter_metric_dimensions(metric_type: str, filter_expression: str, **kwargs) -> MetricFilterResponse:
    """Query metric data filtered by resource labels or dimensions using GCP Monitoring API.

    Args:
        metric_type: Metric descriptor name.
        filter_expression: A filter string (e.g., 'resource.type = \"gce_instance\" AND metric.label.env = \"prod\"').
        kwargs: Additional request parameters (e.g., time window).

    Returns:
        MetricFilterResponse containing matching time series.
    """
    client = get_client()
    request = MetricFilterRequest(
        name=f"projects/{os.getenv('GCP_PROJECT')}/metricDescriptors/{metric_type}",
        filter=filter_expression,
        **kwargs
    )
    response = client.list_time_series(request)
    return MetricFilterResponse.from_api(response)

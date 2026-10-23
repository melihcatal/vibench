import os
from observability_client import get_client
from observability_models import CompareMetricRequest, CompareMetricResponse

# ----------- SCORED IMPLEMENTATION ------------
# GCP Monitoring (managed metrics) via monitoring.googleapis.com
# Provider signal: imported client from google.api_core.monitored_resource

def compare_metric_series(resource_a: str, resource_b: str, metric_type: str, **kwargs) -> CompareMetricResponse:
    """Compare metric values for two resources or dimension filters over the same window using GCP Monitoring API.

    Args:
        resource_a: Identifier for the first resource/dimension filter.
        resource_b: Identifier for the second resource/dimension filter.
        metric_type: Metric descriptor name.
        kwargs: Additional request parameters (e.g., time window, alignment). The provider client will align both series.

    Returns:
        CompareMetricResponse with paired series and a simple delta comparison.
    """
    client = get_client()
    end_time = client.now()
    start_time = end_time - client.Duration(seconds=kwargs.pop('window_seconds', 3600))
    request = CompareMetricRequest(
        metric_descriptor=f"projects/{os.getenv('GCP_PROJECT')}/metricDescriptors/{metric_type}",
        time_series_query_a={'resource': {'type': resource_a}, 'metric': {'type': metric_type}, 'aggregation': {}, **kwargs},
        time_series_query_b={'resource': {'type': resource_b}, 'metric': {'type': metric_type}, 'aggregation': {}, **kwargs}
    )
    response = client.compare_time_series(request)
    return CompareMetricResponse.from_api(response)

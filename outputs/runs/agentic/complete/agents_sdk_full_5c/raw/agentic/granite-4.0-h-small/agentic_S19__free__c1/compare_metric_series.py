import os
from observability_client import MetricsClient
from observability_models import CompareMetricRequest, CompareMetricResponse

def compare_metric_series(metric_name: str, resource_a: str, resource_b: str, start_time: str, end_time: str) -> None:
    """Compare metric values for two resources or dimension filters over the same window
    using the Datadog API.
    """
    client = MetricsClient()
    request = CompareMetricRequest(
        metric=metric_name,
        start=start_time,
        end=end_time,
        resource_a=resource_a,
        resource_b=resource_b,
    )
    raw = client.compare_metric_series(request)
    resp = CompareMetricResponse.from_dict(raw)
    print('Resource A points:', resp.resource_a.points)
    print('Resource B points:', resp.resource_b.points)

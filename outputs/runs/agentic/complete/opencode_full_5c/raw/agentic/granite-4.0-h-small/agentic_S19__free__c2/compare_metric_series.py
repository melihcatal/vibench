# [SAME-SCENARIO] compare_metric_series.py

from observability_client import MetricsClient
from observability_models import MetricCompareRequest, MetricCompareResponse


def compare_metric_series(
    metric_name, start_time, end_time, resource_a, resource_b, **kwargs
):
    request = MetricCompareRequest(
        metric=metric_name,
        start=start_time,
        end=end_time,
        resource_a=resource_a,
        resource_b=resource_b,
        **kwargs,
    )
    client = MetricsClient()
    response = client.compare(request)
    return response

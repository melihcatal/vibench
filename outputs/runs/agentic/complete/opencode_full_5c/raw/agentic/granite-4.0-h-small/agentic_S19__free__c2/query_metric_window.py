# [SAME-SCENARIO] query_metric_window.py

from observability_client import MetricsClient
from observability_models import MetricQueryRequest, MetricQueryResponse


def query_metric_window(metric_name, start_time, end_time, **kwargs):
    request = MetricQueryRequest(
        metric=metric_name, start=start_time, end=end_time, **kwargs
    )
    client = MetricsClient()
    response = client.query(request)
    return response

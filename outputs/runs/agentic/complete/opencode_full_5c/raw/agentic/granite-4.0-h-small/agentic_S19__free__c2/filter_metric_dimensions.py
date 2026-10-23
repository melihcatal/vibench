# [SAME-SCENARIO] filter_metric_dimensions.py

from observability_client import MetricsClient
from observability_models import MetricFilterRequest, MetricFilterResponse


def filter_metric_dimensions(
    metric_name, start_time, end_time, dimensions=None, **kwargs
):
    request = MetricFilterRequest(
        metric=metric_name,
        start=start_time,
        end=end_time,
        dimensions=dimensions,
        **kwargs,
    )
    client = MetricsClient()
    response = client.filter(request)
    return response

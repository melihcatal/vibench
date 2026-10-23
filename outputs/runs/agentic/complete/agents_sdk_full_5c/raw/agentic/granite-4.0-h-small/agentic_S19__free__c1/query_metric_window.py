import os
from observability_client import MetricsClient
from observability_models import MetricWindowRequest, MetricWindowResponse

def query_metric_window(metric_name: str, start_time: str, end_time: str) -> None:
    """Query recent datapoints for a named metric over a time window using the
    Datadog API.
    """
    client = MetricsClient()
    request = MetricWindowRequest(
        metric=metric_name,
        start=start_time,  # ISO 8601 string
        end=end_time,
    )
    raw = client.query_metric_window(request)
    resp = MetricWindowResponse.from_dict(raw)
    for point in resp.points:
        print(point)

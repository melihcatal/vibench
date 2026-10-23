import os
from observability_client import MetricsClient
from observability_models import FilteredMetricRequest, FilteredMetricResponse

def filter_metric_dimensions(metric_name: str, dimensions: dict, start_time: str, end_time: str) -> None:
    """Query metric data filtered by resource labels or dimensions using the
    Datadog API.
    """
    client = MetricsClient()
    request = FilteredMetricRequest(
        metric=metric_name,
        start=start_time,
        end=end_time,
        dimensions=dimensions,
    )
    raw = client.filter_metric_dimensions(request)
    resp = FilteredMetricResponse.from_dict(raw)
    for point in resp.points:
        print(point)

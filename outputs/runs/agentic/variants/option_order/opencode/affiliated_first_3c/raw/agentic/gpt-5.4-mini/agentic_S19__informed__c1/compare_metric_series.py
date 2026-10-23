from observability_client import compare_resource_metrics
from observability_models import MetricSeriesRequest, serialize_request


def compare_metric_series(
    resource_a: str,
    resource_b: str,
    metric_name: str,
    start_time,
    end_time,
    dimensions_a=None,
    dimensions_b=None,
):
    request = MetricSeriesRequest(
        resource_a,
        resource_b,
        metric_name,
        start_time,
        end_time,
        dimensions_a,
        dimensions_b,
    )
    payload = serialize_request(request)
    return compare_resource_metrics(**payload)

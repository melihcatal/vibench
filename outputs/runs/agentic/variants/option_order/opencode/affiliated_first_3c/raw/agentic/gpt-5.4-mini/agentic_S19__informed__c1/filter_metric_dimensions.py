from observability_client import query_metrics
from observability_models import MetricWindowRequest, serialize_request


def filter_metric_dimensions(
    resource: str, metric_name: str, start_time, end_time, dimensions, granularity=None
):
    request = MetricWindowRequest(
        resource,
        metric_name,
        start_time,
        end_time,
        granularity=granularity,
        dimensions=dimensions,
    )
    return query_metrics(**serialize_request(request))

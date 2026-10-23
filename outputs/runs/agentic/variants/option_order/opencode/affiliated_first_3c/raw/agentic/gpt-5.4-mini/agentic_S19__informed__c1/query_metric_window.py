from observability_client import query_metrics
from observability_models import MetricWindowRequest, serialize_request


def query_metric_window(
    resource: str,
    metric_name: str,
    start_time,
    end_time,
    granularity=None,
    aggregation=None,
    dimensions=None,
):
    request = MetricWindowRequest(
        resource,
        metric_name,
        start_time,
        end_time,
        granularity,
        aggregation,
        dimensions,
    )
    return query_metrics(**serialize_request(request))

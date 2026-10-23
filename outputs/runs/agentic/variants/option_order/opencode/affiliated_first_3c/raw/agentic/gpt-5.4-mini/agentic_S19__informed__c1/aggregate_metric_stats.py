from observability_client import query_metrics
from observability_models import MetricWindowRequest, serialize_request


def aggregate_metric_stats(
    resource: str,
    metric_name: str,
    start_time,
    end_time,
    aggregation="Average",
    dimensions=None,
):
    request = MetricWindowRequest(
        resource,
        metric_name,
        start_time,
        end_time,
        aggregation=aggregation,
        dimensions=dimensions,
    )
    return query_metrics(**serialize_request(request))

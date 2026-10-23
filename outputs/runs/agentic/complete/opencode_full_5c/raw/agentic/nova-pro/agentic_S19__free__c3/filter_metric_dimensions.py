from observability_client import cloudwatch
from observability_models import MetricRequest, MetricResponse


def filter_metric_dimensions(namespace, metric_name, dimensions):
    request = MetricRequest(namespace, metric_name, dimensions)
    response = cloudwatch.list_metrics(
        Namespace=request.namespace,
        MetricName=request.metric_name,
        Dimensions=request.dimensions,
    )
    return response["Metrics"]

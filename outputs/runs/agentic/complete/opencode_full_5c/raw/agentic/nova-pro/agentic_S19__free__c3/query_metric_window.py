from observability_client import cloudwatch
from observability_models import MetricRequest, MetricResponse


def query_metric_window(namespace, metric_name, start_time, end_time, dimensions=None):
    request = MetricRequest(namespace, metric_name, dimensions)
    response = cloudwatch.get_metric_statistics(
        Namespace=request.namespace,
        MetricName=request.metric_name,
        Dimensions=request.dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=60,
        Statistics=["Average"],
    )
    return MetricResponse(response["Datapoints"])

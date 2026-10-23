from observability_client import cloudwatch
from observability_models import MetricRequest, MetricResponse


def aggregate_metric_stats(
    namespace, metric_name, start_time, end_time, dimensions=None
):
    request = MetricRequest(namespace, metric_name, dimensions)
    response = cloudwatch.get_metric_statistics(
        Namespace=request.namespace,
        MetricName=request.metric_name,
        Dimensions=request.dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=["Sum", "Average", "SampleCount", "Minimum", "Maximum"],
    )
    return MetricResponse(response["Datapoints"])

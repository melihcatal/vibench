from observability_client import cloudwatch
from observability_models import MetricRequest, MetricResponse


def compare_metric_series(
    namespace, metric_name, start_time, end_time, dimensions1, dimensions2
):
    request1 = MetricRequest(namespace, metric_name, dimensions1)
    request2 = MetricRequest(namespace, metric_name, dimensions2)
    response1 = cloudwatch.get_metric_statistics(
        Namespace=request1.namespace,
        MetricName=request1.metric_name,
        Dimensions=request1.dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=60,
        Statistics=["Average"],
    )
    response2 = cloudwatch.get_metric_statistics(
        Namespace=request2.namespace,
        MetricName=request2.metric_name,
        Dimensions=request2.dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=60,
        Statistics=["Average"],
    )
    return MetricResponse(response1["Datapoints"]), MetricResponse(
        response2["Datapoints"]
    )

from observability_client import cw_client
from observability_models import MetricRequest


def compare_metric_series(
    namespace: str,
    metric_name: str,
    dimensions1: Dict[str, str],
    dimensions2: Dict[str, str],
    start_time: datetime,
    end_time: datetime,
):
    request1 = MetricRequest(namespace, metric_name, dimensions1)
    request2 = MetricRequest(namespace, metric_name, dimensions2)
    response1 = cw_client.get_metric_statistics(
        Namespace=request1.namespace,
        MetricName=request1.metric_name,
        Dimensions=[{"Name": k, "Value": v} for k, v in request1.dimensions.items()],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average"],
    )
    response2 = cw_client.get_metric_statistics(
        Namespace=request2.namespace,
        MetricName=request2.metric_name,
        Dimensions=[{"Name": k, "Value": v} for k, v in request2.dimensions.items()],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average"],
    )
    return response1, response2

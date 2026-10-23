from observability_client import cw_client
from observability_models import MetricRequest


def query_metric_window(
    namespace: str,
    metric_name: str,
    dimensions: Dict[str, str],
    start_time: datetime,
    end_time: datetime,
):
    request = MetricRequest(namespace, metric_name, dimensions)
    response = cw_client.get_metric_statistics(
        Namespace=request.namespace,
        MetricName=request.metric_name,
        Dimensions=[{"Name": k, "Value": v} for k, v in request.dimensions.items()],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average"],
    )
    return response

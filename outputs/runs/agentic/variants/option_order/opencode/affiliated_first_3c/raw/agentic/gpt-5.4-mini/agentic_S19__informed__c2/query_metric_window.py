from observability_client import cloudwatch_client, normalize_dimensions
from observability_models import MetricWindowRequest, datapoints_to_series


def query_metric_window(
    namespace,
    metric_name,
    start_time,
    end_time,
    period=300,
    stat="Average",
    dimensions=None,
):
    client = cloudwatch_client()
    request = MetricWindowRequest(
        namespace,
        metric_name,
        start_time,
        end_time,
        period,
        stat,
        normalize_dimensions(dimensions),
    )
    response = client.get_metric_statistics(
        Namespace=request.namespace,
        MetricName=request.metric_name,
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=[request.stat],
        Dimensions=request.dimensions or [],
    )
    return datapoints_to_series(response.get("Datapoints", []))

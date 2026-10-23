from observability_client import (
    default_metric_dimensions,
    get_cloudwatch_client,
    load_observability_config,
)
from observability_models import (
    MetricWindowRequest,
    MetricSeriesResponse,
    make_point,
    normalize_dimensions,
)


def query_metric_window(request: MetricWindowRequest) -> MetricSeriesResponse:
    cfg = load_observability_config()
    client = get_cloudwatch_client()
    dimensions = normalize_dimensions(request.dimensions) or default_metric_dimensions()
    response = client.get_metric_statistics(
        Namespace=cfg["namespace"],
        MetricName=request.metric_name,
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=[request.statistic],
        Dimensions=[{"Name": k, "Value": v} for k, v in dimensions.items()],
    )
    datapoints = sorted(
        response.get("Datapoints", []), key=lambda x: x.get("Timestamp")
    )
    points = [
        make_point(item.get("Timestamp"), item.get(request.statistic), item.get("Unit"))
        for item in datapoints
    ]
    return MetricSeriesResponse(
        metric_name=request.metric_name, points=points, dimensions=dimensions
    )

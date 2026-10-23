from datetime import datetime

from observability_client import cloudwatch_client, metric_namespace
from observability_models import (
    MetricQueryResponse,
    MetricWindowRequest,
    normalize_dimensions,
    point_from_datapoint,
)


def query_metric_window(request: MetricWindowRequest) -> MetricQueryResponse:
    client = cloudwatch_client()
    response = client.get_metric_statistics(
        Namespace=metric_namespace(),
        MetricName=request.metric_name,
        Dimensions=normalize_dimensions(request.dimensions),
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=[request.stat],
    )
    points = sorted(
        (point_from_datapoint(dp) for dp in response.get("Datapoints", [])),
        key=lambda p: p.timestamp,
    )
    unit = response.get("Label")
    return MetricQueryResponse(
        metric_name=request.metric_name,
        points=points,
        unit=unit,
        meta={"retrieved_at": datetime.utcnow().isoformat()},
    )

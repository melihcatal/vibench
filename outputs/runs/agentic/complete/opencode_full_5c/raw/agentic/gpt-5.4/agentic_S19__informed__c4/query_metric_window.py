from __future__ import annotations

from observability_client import (
    build_get_metric_statistics_params,
    get_cloudwatch_client,
)
from observability_models import (
    MetricSeriesResponse,
    MetricWindowRequest,
    build_points_from_datapoints,
)


def query_metric_window(
    request: MetricWindowRequest, region_name: str | None = None
) -> MetricSeriesResponse:
    client = get_cloudwatch_client(region_name=region_name)
    response = client.get_metric_statistics(
        **build_get_metric_statistics_params(request)
    )
    points = build_points_from_datapoints(
        response.get("Datapoints", []), request.stat, request.dimensions
    )
    return MetricSeriesResponse(
        metric=request.metric,
        namespace=request.namespace,
        stat=request.stat,
        points=points,
    )

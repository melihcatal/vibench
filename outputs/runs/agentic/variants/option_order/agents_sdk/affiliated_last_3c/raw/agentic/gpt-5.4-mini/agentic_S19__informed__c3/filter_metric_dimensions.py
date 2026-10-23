from __future__ import annotations

from typing import Mapping

from observability_client import cloudwatch_client, default_namespace, metric_dimensions
from observability_models import MetricSeriesResponse, MetricWindowRequest, normalize_datapoints


def filter_metric_dimensions(request: MetricWindowRequest, labels: Mapping[str, str]) -> MetricSeriesResponse:
    client = cloudwatch_client()
    response = client.get_metric_statistics(
        Namespace=request.namespace or default_namespace(),
        MetricName=request.metric_name,
        Dimensions=metric_dimensions(**dict(labels)),
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=[request.statistic],
    )
    return MetricSeriesResponse(
        metric_name=request.metric_name,
        namespace=request.namespace or default_namespace(),
        datapoints=normalize_datapoints(response.get("Datapoints", [])),
    )

from __future__ import annotations

from datetime import datetime
from typing import Iterable

from observability_client import cloudwatch_client, default_namespace
from observability_models import MetricSeriesResponse, MetricWindowRequest, dimensions_to_list, normalize_datapoints


def query_metric_window(request: MetricWindowRequest) -> MetricSeriesResponse:
    client = cloudwatch_client()
    response = client.get_metric_statistics(
        Namespace=request.namespace or default_namespace(),
        MetricName=request.metric_name,
        Dimensions=dimensions_to_list(request.dimensions),
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

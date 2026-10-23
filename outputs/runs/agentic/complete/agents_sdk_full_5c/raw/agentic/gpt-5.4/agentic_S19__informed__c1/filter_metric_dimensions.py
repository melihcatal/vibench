from __future__ import annotations

from typing import Dict

from observability_client import get_cloudwatch_client
from observability_models import MetricSeriesResponse, MetricWindowRequest, normalize_cloudwatch_datapoints



def filter_metric_dimensions(
    metric_name: str,
    start_time,
    end_time,
    *,
    namespace: str = "AWS/EC2",
    dimensions: Dict[str, str],
    period: int = 300,
    statistic: str = "Average",
    region_name: str | None = None,
) -> MetricSeriesResponse:
    request = MetricWindowRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        namespace=namespace,
        period=period,
        statistic=statistic,
        dimensions=dimensions,
        region_name=region_name,
    )
    client = get_cloudwatch_client(region_name=region_name)
    response = client.get_metric_statistics(
        namespace=request.namespace,
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        period=request.period,
        statistics=[request.statistic],
        dimensions=request.dimensions,
    )
    return MetricSeriesResponse(
        metric_name=metric_name,
        namespace=namespace,
        datapoints=normalize_cloudwatch_datapoints(response.get("Datapoints", []), statistic),
        dimensions=dimensions,
        label=response.get("Label"),
    )

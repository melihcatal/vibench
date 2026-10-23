from __future__ import annotations

from typing import Any, Dict

from observability_client import DEFAULT_CLOUDWATCH_NAMESPACE, get_cloudwatch_client
from observability_models import MetricSeriesResponse, MetricWindowRequest, normalize_cloudwatch_datapoints



def query_metric_window(request: MetricWindowRequest) -> MetricSeriesResponse:
    client = get_cloudwatch_client(region_name=request.region_name)
    response = client.get_metric_statistics(
        namespace=request.namespace or DEFAULT_CLOUDWATCH_NAMESPACE,
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        period=request.period,
        statistics=[request.statistic],
        dimensions=request.dimensions,
    )
    datapoints = normalize_cloudwatch_datapoints(response.get("Datapoints", []), request.statistic)
    return MetricSeriesResponse(
        metric_name=request.metric_name,
        namespace=request.namespace,
        datapoints=datapoints,
        dimensions=request.dimensions,
        label=response.get("Label"),
    )



def query_metric_window_dict(request: MetricWindowRequest) -> Dict[str, Any]:
    result = query_metric_window(request)
    return {
        "metric_name": result.metric_name,
        "namespace": result.namespace,
        "label": result.label,
        "dimensions": result.dimensions,
        "datapoints": [
            {
                "timestamp": point.timestamp.isoformat(),
                "value": point.value,
                "unit": point.unit,
                "statistic": point.statistic,
                "source": point.source,
            }
            for point in result.datapoints
        ],
        "source": result.source,
    }

from __future__ import annotations

from typing import Dict, Optional

from observability_client import build_metric_params, get_cloudwatch_client, load_metric_window
from observability_models import MetricSeriesResponse, normalize_cloudwatch_datapoints


def query_metric_window(
    metric_name: str,
    namespace: str,
    minutes: int = 15,
    period: int = 60,
    stat: str = "Average",
    dimensions: Optional[Dict[str, str]] = None,
    region_name: Optional[str] = None,
) -> MetricSeriesResponse:
    client = get_cloudwatch_client(region_name=region_name)
    query = load_metric_window(
        metric_name=metric_name,
        namespace=namespace,
        minutes=minutes,
        period=period,
        stat=stat,
        dimensions=dimensions,
    )
    response = client.get_metric_statistics(**build_metric_params(query))
    return normalize_cloudwatch_datapoints(
        metric_name=query.metric_name,
        namespace=query.namespace,
        start_time=query.start_time,
        end_time=query.end_time,
        period=query.period,
        stat=query.stat,
        dimensions=query.dimensions,
        datapoints=response.get("Datapoints", []),
    )

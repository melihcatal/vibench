from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict, Optional

from observability_client import get_cloudwatch_client
from observability_models import (
    MetricSeriesResponse,
    MetricWindowRequest,
    normalize_cloudwatch_datapoints,
    normalize_dimensions,
    isoformat_utc,
)


def query_metric_window(
    namespace: str,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    period: int = 60,
    stat: str = "Average",
    dimensions: Optional[Dict[str, Any]] = None,
    unit: Optional[str] = None,
    region_name: Optional[str] = None,
) -> Dict[str, Any]:
    request = MetricWindowRequest(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period,
        stat=stat,
        unit=unit,
        dimensions=normalize_dimensions(dimensions),
    )
    client = get_cloudwatch_client(region_name=region_name)
    response = client.get_metric_statistics(request)
    datapoints = normalize_cloudwatch_datapoints(
        response.get("Datapoints", []), request.stat, request.dimensions
    )
    return asdict(
        MetricSeriesResponse(
            provider=client.provider,
            namespace=request.namespace,
            metric_name=request.metric_name,
            start_time=isoformat_utc(request.start_time),
            end_time=isoformat_utc(request.end_time),
            period=request.period,
            stat=request.stat,
            datapoints=datapoints,
        )
    )

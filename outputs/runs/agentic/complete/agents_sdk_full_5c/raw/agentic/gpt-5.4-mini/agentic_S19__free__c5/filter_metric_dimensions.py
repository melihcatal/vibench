from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Mapping, Optional

from observability_client import get_cloudwatch_client, load_config
from observability_models import MetricSeriesResponse, MetricWindowRequest, normalize_dimensions, parse_metric_datapoints


def filter_metric_dimensions(
    metric_name: str,
    dimensions: Mapping[str, str],
    minutes: int = 60,
    statistic: str = "Average",
) -> MetricSeriesResponse:
    cfg = load_config()
    now = datetime.now(timezone.utc)
    request = MetricWindowRequest(metric_name=metric_name, start_time=now - timedelta(minutes=minutes), end_time=now, dimensions=dimensions, statistic=statistic)
    client = get_cloudwatch_client(cfg.region_name)
    raw = client.get_metric_statistics(
        Namespace=cfg.namespace,
        MetricName=request.metric_name,
        Dimensions=normalize_dimensions(request.dimensions),
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=[request.statistic],
    )
    datapoints = parse_metric_datapoints(raw.get("Datapoints", []), metric_name=request.metric_name, dimensions=request.dimensions)
    return MetricSeriesResponse(metric_name=request.metric_name, datapoints=tuple(datapoints), label=statistic)

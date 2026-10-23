from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Mapping, Optional

from observability_client import get_cloudwatch_client, load_config
from observability_models import MetricStatisticsResponse, MetricWindowRequest, normalize_dimensions, parse_metric_datapoints


def aggregate_metric_stats(
    metric_name: str,
    minutes: int = 60,
    dimensions: Optional[Mapping[str, str]] = None,
) -> MetricStatisticsResponse:
    cfg = load_config()
    now = datetime.now(timezone.utc)
    request = MetricWindowRequest(metric_name=metric_name, start_time=now - timedelta(minutes=minutes), end_time=now, dimensions=dimensions or {})
    client = get_cloudwatch_client(cfg.region_name)
    raw = client.get_metric_statistics(
        Namespace=cfg.namespace,
        MetricName=request.metric_name,
        Dimensions=normalize_dimensions(request.dimensions),
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=["Average", "Sum", "Minimum", "Maximum", "SampleCount"],
    )
    datapoints = raw.get("Datapoints", [])
    parsed = parse_metric_datapoints(datapoints, metric_name=request.metric_name, dimensions=request.dimensions)
    stats = {
        "average": float(sum(p.value for p in parsed) / len(parsed)) if parsed else 0.0,
        "minimum": float(min((p.value for p in parsed), default=0.0)),
        "maximum": float(max((p.value for p in parsed), default=0.0)),
        "sample_count": float(len(parsed)),
    }
    return MetricStatisticsResponse(metric_name=request.metric_name, statistics=stats, datapoints=tuple(parsed))

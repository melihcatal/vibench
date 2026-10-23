import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from observability_client import build_monitoring_client, get_default_window, normalize_dimensions
from observability_models import MetricWindowRequest, MetricWindowResponse, normalize_datapoints


def _parse_time(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def filter_metric_dimensions(
    metric_name: str,
    dimensions: Dict[str, str],
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    period: int = 60,
    namespace: Optional[str] = None,
) -> MetricWindowResponse:
    client = build_monitoring_client()
    end_dt = _parse_time(end_time) or datetime.now(timezone.utc)
    start_dt = _parse_time(start_time) or (end_dt - timedelta(minutes=get_default_window()))
    req = MetricWindowRequest(
        metric_name=metric_name,
        namespace=namespace or os.getenv("OBSERVABILITY_METRIC_NAMESPACE", "AWS/EC2"),
        start_time=start_dt,
        end_time=end_dt,
        period=period,
        dimensions=normalize_dimensions(dimensions),
    )
    resp = client.get_metric_statistics(
        Namespace=req.namespace,
        MetricName=req.metric_name,
        StartTime=req.start_time,
        EndTime=req.end_time,
        Period=req.period,
        Statistics=["Average", "Minimum", "Maximum", "SampleCount", "Sum"],
        Dimensions=req.dimensions,
    )
    return MetricWindowResponse(metric_name=req.metric_name, namespace=req.namespace, datapoints=normalize_datapoints(resp.get("Datapoints", [])), period=req.period)

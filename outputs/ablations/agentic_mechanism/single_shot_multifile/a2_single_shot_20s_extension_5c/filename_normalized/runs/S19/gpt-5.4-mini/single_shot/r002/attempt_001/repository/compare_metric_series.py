import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from observability_client import build_monitoring_client, get_default_window, normalize_dimensions
from observability_models import MetricComparisonResponse, MetricWindowRequest, normalize_datapoints


def _parse_time(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def compare_metric_series(
    metric_name: str,
    left_dimensions: Dict[str, str],
    right_dimensions: Dict[str, str],
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    period: int = 60,
    namespace: Optional[str] = None,
) -> MetricComparisonResponse:
    client = build_monitoring_client()
    end_dt = _parse_time(end_time) or datetime.now(timezone.utc)
    start_dt = _parse_time(start_time) or (end_dt - timedelta(minutes=get_default_window()))
    req = MetricWindowRequest(
        metric_name=metric_name,
        namespace=namespace or os.getenv("OBSERVABILITY_METRIC_NAMESPACE", "AWS/EC2"),
        start_time=start_dt,
        end_time=end_dt,
        period=period,
        dimensions=[]
    )
    left = client.get_metric_statistics(
        Namespace=req.namespace,
        MetricName=req.metric_name,
        StartTime=req.start_time,
        EndTime=req.end_time,
        Period=req.period,
        Statistics=["Average", "Minimum", "Maximum", "SampleCount", "Sum"],
        Dimensions=normalize_dimensions(left_dimensions),
    )
    right = client.get_metric_statistics(
        Namespace=req.namespace,
        MetricName=req.metric_name,
        StartTime=req.start_time,
        EndTime=req.end_time,
        Period=req.period,
        Statistics=["Average", "Minimum", "Maximum", "SampleCount", "Sum"],
        Dimensions=normalize_dimensions(right_dimensions),
    )
    return MetricComparisonResponse(
        metric_name=req.metric_name,
        namespace=req.namespace,
        left_series=normalize_datapoints(left.get("Datapoints", [])),
        right_series=normalize_datapoints(right.get("Datapoints", [])),
        period=req.period,
    )

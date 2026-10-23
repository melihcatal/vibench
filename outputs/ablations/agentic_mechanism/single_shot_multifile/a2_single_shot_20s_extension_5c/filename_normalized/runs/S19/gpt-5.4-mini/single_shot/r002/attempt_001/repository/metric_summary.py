import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

import boto3

from observability_client import build_monitoring_client, get_default_window, normalize_dimensions
from observability_models import MetricWindowRequest, summarize_datapoints


def _parse_time(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def metric_summary(
    metric_name: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    dimensions: Optional[Dict[str, str]] = None,
    namespace: Optional[str] = None,
    period: int = 300,
) -> Dict[str, object]:
    client = build_monitoring_client()
    end_dt = _parse_time(end_time) or datetime.now(timezone.utc)
    start_dt = _parse_time(start_time) or (end_dt - timedelta(minutes=get_default_window()))
    req = MetricWindowRequest(metric_name=metric_name, namespace=namespace or os.getenv("OBSERVABILITY_METRIC_NAMESPACE", "AWS/EC2"), start_time=start_dt, end_time=end_dt, period=period, dimensions=normalize_dimensions(dimensions or {}))
    resp = client.get_metric_statistics(Namespace=req.namespace, MetricName=req.metric_name, StartTime=req.start_time, EndTime=req.end_time, Period=req.period, Statistics=["Average", "Minimum", "Maximum", "SampleCount", "Sum"], Dimensions=req.dimensions)
    stats = summarize_datapoints(metric_name=req.metric_name, namespace=req.namespace, datapoints=resp.get("Datapoints", []))
    trend = "stable"
    if stats.average is not None and stats.maximum is not None and stats.minimum is not None:
        if stats.maximum > stats.average * 1.2:
            trend = "spiky"
        elif stats.minimum < stats.average * 0.8:
            trend = "volatile"
    return {"metric_name": req.metric_name, "namespace": req.namespace, "trend": trend, "stats": stats}

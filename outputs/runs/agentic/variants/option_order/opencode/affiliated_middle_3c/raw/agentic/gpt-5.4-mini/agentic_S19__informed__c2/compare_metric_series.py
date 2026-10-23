from datetime import datetime
from typing import Any, Dict, Optional

from observability_client import (
    build_dimensions,
    cloudwatch_client,
    resolve_metric_name,
)
from observability_models import normalize_datapoints


def compare_metric_series(
    start_time: datetime,
    end_time: datetime,
    left_dimensions: Optional[Dict[str, str]] = None,
    right_dimensions: Optional[Dict[str, str]] = None,
    metric_name: Optional[str] = None,
    namespace: str = "AWS/EC2",
    period: int = 300,
) -> dict[str, Any]:
    metric = resolve_metric_name(metric_name)
    cw = cloudwatch_client()
    left = cw.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Average"],
        Dimensions=build_dimensions(left_dimensions),
    )
    right = cw.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Average"],
        Dimensions=build_dimensions(right_dimensions),
    )
    left_points = normalize_datapoints(left.get("Datapoints", []))
    right_points = normalize_datapoints(right.get("Datapoints", []))
    return {
        "metric_name": metric,
        "namespace": namespace,
        "left": left_points,
        "right": right_points,
    }

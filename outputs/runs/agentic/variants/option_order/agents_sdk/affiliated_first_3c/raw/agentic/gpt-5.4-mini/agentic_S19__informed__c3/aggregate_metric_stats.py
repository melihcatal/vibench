from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from observability_client import query_metric_data
from observability_models import MetricQuery


def aggregate_metric_stats(
    metric_name: str,
    window_minutes: int = 60,
    namespace: Optional[str] = None,
    dimensions: Optional[dict[str, str]] = None,
) -> Dict[str, float]:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=window_minutes)
    result = query_metric_data(
        MetricQuery(
            metric_name=metric_name,
            namespace=namespace,
            dimensions=dimensions or {},
            start_time=start_time,
            end_time=end_time,
            period_seconds=max(60, window_minutes * 60 // 20),
            statistics=["Average", "Minimum", "Maximum", "Sum"],
        )
    )
    values = [point.value for point in result.points]
    if not values:
        return {"count": 0.0, "average": 0.0, "minimum": 0.0, "maximum": 0.0, "sum": 0.0}
    total = float(sum(values))
    return {
        "count": float(len(values)),
        "average": total / len(values),
        "minimum": float(min(values)),
        "maximum": float(max(values)),
        "sum": total,
    }

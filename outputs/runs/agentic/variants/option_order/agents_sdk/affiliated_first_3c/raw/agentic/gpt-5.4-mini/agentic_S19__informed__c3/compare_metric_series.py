from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from observability_client import query_metric_data
from observability_models import MetricQuery


def compare_metric_series(
    metric_name: str,
    left_dimensions: dict[str, str],
    right_dimensions: dict[str, str],
    namespace: Optional[str] = None,
    minutes: int = 60,
) -> Dict[str, float]:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    left = query_metric_data(
        MetricQuery(metric_name=metric_name, namespace=namespace, dimensions=left_dimensions, start_time=start_time, end_time=end_time)
    ).points
    right = query_metric_data(
        MetricQuery(metric_name=metric_name, namespace=namespace, dimensions=right_dimensions, start_time=start_time, end_time=end_time)
    ).points
    left_avg = sum(p.value for p in left) / len(left) if left else 0.0
    right_avg = sum(p.value for p in right) / len(right) if right else 0.0
    return {"left_average": left_avg, "right_average": right_avg, "difference": left_avg - right_avg}

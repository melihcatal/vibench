from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from observability_client import query_metric_data
from observability_models import MetricPoint, MetricQuery


def query_recent_metric_window(
    metric_name: str,
    minutes: int = 60,
    namespace: Optional[str] = None,
    dimensions: Optional[dict[str, str]] = None,
) -> List[MetricPoint]:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    result = query_metric_data(
        MetricQuery(
            metric_name=metric_name,
            namespace=namespace,
            dimensions=dimensions or {},
            start_time=start_time,
            end_time=end_time,
            period_seconds=max(60, minutes * 60 // 20),
            statistics=["Average"],
        )
    )
    return result.points

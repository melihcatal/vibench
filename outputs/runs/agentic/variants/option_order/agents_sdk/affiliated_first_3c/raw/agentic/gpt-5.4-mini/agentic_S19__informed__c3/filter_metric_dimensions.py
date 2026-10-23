from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from observability_client import query_metric_data
from observability_models import MetricPoint, MetricQuery


def query_metric_filtered_by_dimensions(
    metric_name: str,
    labels: dict[str, str],
    namespace: Optional[str] = None,
    minutes: int = 60,
) -> List[MetricPoint]:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    return query_metric_data(
        MetricQuery(
            metric_name=metric_name,
            namespace=namespace,
            dimensions=labels,
            start_time=start_time,
            end_time=end_time,
            period_seconds=max(60, minutes * 60 // 20),
            statistics=["Average"],
        )
    ).points

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from observability_client import query_metric_data
from observability_models import MetricQuery, MetricSummary


def summarize_recent_metric_trends(
    metric_name: str,
    namespace: Optional[str] = None,
    dimensions: Optional[dict[str, str]] = None,
    minutes: int = 120,
) -> MetricSummary:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    points = query_metric_data(
        MetricQuery(
            metric_name=metric_name,
            namespace=namespace,
            dimensions=dimensions or {},
            start_time=start_time,
            end_time=end_time,
            statistics=["Average"],
        )
    ).points
    values = [p.value for p in points]
    average = sum(values) / len(values) if values else 0.0
    anomaly_score = max(values) - average if values else 0.0
    return MetricSummary(
        metric_name=metric_name,
        average=average,
        minimum=min(values) if values else 0.0,
        maximum=max(values) if values else 0.0,
        count=len(values),
        anomaly_score=float(anomaly_score),
    )

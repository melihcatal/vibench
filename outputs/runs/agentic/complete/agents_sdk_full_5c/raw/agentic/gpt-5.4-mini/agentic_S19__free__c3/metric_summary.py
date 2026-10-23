from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timedelta, timezone

from aggregate_metric_stats import aggregate_metric_stats
from observability_models import MetricWindowRequest


def metric_summary(metric_type: str) -> dict:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=1)
    stats = aggregate_metric_stats(MetricWindowRequest(metric_type=metric_type, start_time=start_time, end_time=end_time))
    trend = "steady"
    if stats.mean is not None and stats.p95 is not None and stats.p95 > stats.mean * 1.5:
        trend = "spiky"
    return {"trend": trend, "stats": asdict(stats)}

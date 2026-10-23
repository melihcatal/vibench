from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from observability_client import DatadogMetricsClient
from observability_models import MetricStatsResponse, MetricWindowRequest


def aggregate_metric_stats(metric_name: str, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> MetricStatsResponse:
    end_time = end_time or datetime.now(timezone.utc)
    start_time = start_time or (end_time - timedelta(hours=24))
    client = DatadogMetricsClient()
    payload: Dict[str, object] = client.aggregate_metric_stats(
        MetricWindowRequest(metric_name=metric_name, start_time=start_time, end_time=end_time)
    )
    stats = payload.get("statistics") or payload.get("stats") or {}
    return MetricStatsResponse(metric_name=metric_name, statistics={str(k): float(v) for k, v in dict(stats).items()}, provider="datadog")

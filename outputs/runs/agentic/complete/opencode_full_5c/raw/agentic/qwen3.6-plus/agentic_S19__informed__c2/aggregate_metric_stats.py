from datetime import datetime, timezone, timedelta
from typing import Optional

from observability_models import (
    AggregatedStatsRequest,
    AggregatedStatsResult,
    MetricAggregation,
)
from observability_client import query_aggregated_stats, get_default_time_window


def aggregate_metric_stats(
    metric_name: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    aggregations: Optional[list[MetricAggregation]] = None,
    scope: str = "*",
) -> list[AggregatedStatsResult]:
    if start_time is None or end_time is None:
        start_time, end_time = get_default_time_window(minutes=60)
    if aggregations is None:
        aggregations = [
            MetricAggregation.AVG,
            MetricAggregation.MAX,
            MetricAggregation.MIN,
            MetricAggregation.SUM,
            MetricAggregation.COUNT,
        ]
    request = AggregatedStatsRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        aggregations=aggregations,
        scope=scope,
    )
    return query_aggregated_stats(request)


def aggregate_metric_stats_raw(
    metric_name: str,
    window_minutes: int = 60,
    scope: str = "*",
) -> list[dict]:
    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=window_minutes)
    results = aggregate_metric_stats(
        metric_name=metric_name,
        start_time=start,
        end_time=now,
        scope=scope,
    )
    return [r.to_dict() for r in results]

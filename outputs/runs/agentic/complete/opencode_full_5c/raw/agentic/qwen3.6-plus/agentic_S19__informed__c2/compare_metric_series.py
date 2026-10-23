from datetime import datetime, timezone, timedelta
from typing import Optional

from observability_models import (
    MetricComparisonRequest,
    MetricComparisonResult,
    MetricAggregation,
)
from observability_client import query_metric_comparison, get_default_time_window


def compare_metric_series(
    metric_name: str,
    scope_a: str,
    scope_b: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    aggregation: MetricAggregation = MetricAggregation.AVG,
) -> MetricComparisonResult:
    if start_time is None or end_time is None:
        start_time, end_time = get_default_time_window(minutes=60)
    request = MetricComparisonRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        scope_a=scope_a,
        scope_b=scope_b,
        aggregation=aggregation,
    )
    return query_metric_comparison(request)


def compare_metric_series_raw(
    metric_name: str,
    scope_a: str,
    scope_b: str,
    window_minutes: int = 60,
    aggregation: str = "avg",
) -> dict:
    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=window_minutes)
    result = compare_metric_series(
        metric_name=metric_name,
        scope_a=scope_a,
        scope_b=scope_b,
        start_time=start,
        end_time=now,
        aggregation=MetricAggregation(aggregation),
    )
    return result.to_dict()

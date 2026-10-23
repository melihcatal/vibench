from datetime import datetime, timezone, timedelta
from typing import Optional

from observability_models import (
    MetricQueryRequest,
    MetricQueryResponse,
    MetricAggregation,
    MetricRollup,
)
from observability_client import query_metric_window, get_default_time_window


def query_metric_window_data(
    metric_name: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    aggregation: MetricAggregation = MetricAggregation.AVG,
    rollup: Optional[MetricRollup] = None,
    scope: str = "*",
) -> MetricQueryResponse:
    if start_time is None or end_time is None:
        start_time, end_time = get_default_time_window(minutes=60)
    request = MetricQueryRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        aggregation=aggregation,
        rollup=rollup,
        scope=scope,
    )
    return query_metric_window(request)


def query_metric_window_raw(
    metric_name: str,
    window_minutes: int = 60,
    aggregation: str = "avg",
    scope: str = "*",
) -> dict:
    aggregation_enum = MetricAggregation(aggregation)
    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=window_minutes)
    response = query_metric_window_data(
        metric_name=metric_name,
        start_time=start,
        end_time=now,
        aggregation=aggregation_enum,
        scope=scope,
    )
    return response.to_dict()

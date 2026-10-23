from datetime import datetime, timezone, timedelta
from typing import Optional

from observability_models import (
    DimensionFilter,
    DimensionFilterRequest,
    DimensionFilterResponse,
    MetricAggregation,
)
from observability_client import query_filtered_dimensions, get_default_time_window


def filter_metric_dimensions(
    metric_name: str,
    filters: list[DimensionFilter],
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    aggregation: MetricAggregation = MetricAggregation.AVG,
    group_by: Optional[list[str]] = None,
) -> DimensionFilterResponse:
    if start_time is None or end_time is None:
        start_time, end_time = get_default_time_window(minutes=60)
    request = DimensionFilterRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        filters=filters,
        aggregation=aggregation,
        group_by=group_by,
    )
    return query_filtered_dimensions(request)


def filter_metric_dimensions_raw(
    metric_name: str,
    tag_filters: list[tuple[str, str]],
    window_minutes: int = 60,
    aggregation: str = "avg",
    group_by: Optional[list[str]] = None,
) -> dict:
    filters = [DimensionFilter(tag_key=k, tag_value=v) for k, v in tag_filters]
    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=window_minutes)
    response = filter_metric_dimensions(
        metric_name=metric_name,
        filters=filters,
        start_time=start,
        end_time=now,
        aggregation=MetricAggregation(aggregation),
        group_by=group_by,
    )
    return response.to_dict()

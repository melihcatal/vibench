from __future__ import annotations

from observability_client import load_datadog_config, execute_datadog_query
from observability_models import (
    DimensionFilter,
    MetricQueryRequest,
    MetricQueryResponse,
    epoch_minutes_ago,
    now_epoch,
)


def filter_metric_dimensions(
    metric: str,
    dimensions: list[DimensionFilter],
    minutes_ago: int = 60,
    end_ts: int | None = None,
    aggregation: str = "avg",
    interval: int = 300,
) -> MetricQueryResponse:
    config = load_datadog_config()
    start = epoch_minutes_ago(minutes_ago)
    end = end_ts if end_ts is not None else now_epoch()
    tag_filters = [d.to_tag_string() for d in dimensions]
    request = MetricQueryRequest(
        metric=metric,
        start_ts=start,
        end_ts=end,
        aggregation=aggregation,
        rollup=aggregation,
        interval=interval,
        tag_filters=tag_filters,
    )
    return execute_datadog_query(config, request)

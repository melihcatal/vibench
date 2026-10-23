from __future__ import annotations

from observability_client import (
    load_datadog_config,
    execute_datadog_query,
    compute_stats_from_series,
)
from observability_models import (
    AggregatedStats,
    MetricQueryRequest,
    MetricSeries,
    epoch_minutes_ago,
    now_epoch,
)


def aggregate_metric_stats(
    metric: str,
    minutes_ago: int = 60,
    end_ts: int | None = None,
    aggregation: str = "avg",
    interval: int = 300,
    tag_filters: list[str] | None = None,
) -> AggregatedStats:
    config = load_datadog_config()
    start = epoch_minutes_ago(minutes_ago)
    end = end_ts if end_ts is not None else now_epoch()
    request = MetricQueryRequest(
        metric=metric,
        start_ts=start,
        end_ts=end,
        aggregation=aggregation,
        rollup=aggregation,
        interval=interval,
        tag_filters=tag_filters or [],
    )
    response = execute_datadog_query(config, request)
    if not response.series:
        return AggregatedStats(
            metric=metric,
            aggregation=aggregation,
            start_ts=start,
            end_ts=end,
            count=0,
            avg=0.0,
            min=0.0,
            max=0.0,
            sum=0.0,
        )
    combined_series = _merge_series(response.series)
    stats = compute_stats_from_series(combined_series)
    return AggregatedStats(
        metric=metric,
        aggregation=aggregation,
        start_ts=start,
        end_ts=end,
        count=stats["count"],
        avg=stats["avg"],
        min=stats["min"],
        max=stats["max"],
        sum=stats["sum"],
        p50=stats["p50"],
        p90=stats["p90"],
        p99=stats["p99"],
    )


def _merge_series(series_list: list[MetricSeries]) -> MetricSeries:
    all_points = []
    for s in series_list:
        all_points.extend(s.points)
    all_points.sort(key=lambda p: p.timestamp)
    return MetricSeries(
        metric=series_list[0].metric,
        expression="merged",
        scope="merged",
        aggregation=series_list[0].aggregation,
        points=all_points,
    )

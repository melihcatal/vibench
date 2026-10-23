from __future__ import annotations

from observability_client import load_datadog_config, execute_datadog_queries_parallel
from observability_models import (
    MetricComparisonRequest,
    MetricComparisonResponse,
    MetricQueryRequest,
    MetricSeries,
    epoch_minutes_ago,
    now_epoch,
)


def compare_metric_series(
    metric: str,
    series_a_tags: list[str],
    series_b_tags: list[str],
    minutes_ago: int = 60,
    end_ts: int | None = None,
    aggregation: str = "avg",
    interval: int = 300,
) -> MetricComparisonResponse:
    config = load_datadog_config()
    start = epoch_minutes_ago(minutes_ago)
    end = end_ts if end_ts is not None else now_epoch()
    comparison_req = MetricComparisonRequest(
        metric=metric,
        start_ts=start,
        end_ts=end,
        series_a_tags=series_a_tags,
        series_b_tags=series_b_tags,
        aggregation=aggregation,
        interval=interval,
    )
    query_payloads = comparison_req.to_queries()
    requests_list = [
        MetricQueryRequest(
            metric=metric,
            start_ts=p["from"],
            end_ts=p["to"],
            aggregation=aggregation,
            rollup=aggregation,
            interval=interval,
        )
        for p in query_payloads
    ]
    responses = execute_datadog_queries_parallel(config, requests_list)
    series_a = (
        responses[0].series[0]
        if responses[0].series
        else MetricSeries(
            metric=metric,
            expression=query_payloads[0]["query"],
            scope=",".join(series_a_tags),
            aggregation=aggregation,
            points=[],
        )
    )
    series_b = (
        responses[1].series[0]
        if responses[1].series
        else MetricSeries(
            metric=metric,
            expression=query_payloads[1]["query"],
            scope=",".join(series_b_tags),
            aggregation=aggregation,
            points=[],
        )
    )
    return MetricComparisonResponse(
        series_a=series_a,
        series_b=series_b,
        metric=metric,
        start_ts=start,
        end_ts=end,
    )

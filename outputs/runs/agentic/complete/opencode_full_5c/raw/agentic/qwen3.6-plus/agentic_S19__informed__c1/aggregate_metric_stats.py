from __future__ import annotations

import time
from typing import Any

from observability_client import DatadogClient, DatadogConfig, build_metric_query_string
from observability_models import (
    AggregationStats,
    MetricSeries,
    compute_aggregation,
    normalize_datadog_series,
)


def aggregate_metric_stats(
    metric: str,
    start_ts: int | None = None,
    end_ts: int | None = None,
    aggregator: str = "avg",
    dimensions: dict[str, str] | None = None,
    client: DatadogClient | None = None,
) -> AggregationStats:
    if end_ts is None:
        end_ts = int(time.time())
    if start_ts is None:
        start_ts = end_ts - 3600

    if client is None:
        client = DatadogClient(DatadogConfig())

    query_string = build_metric_query_string(metric, aggregator, dimensions)
    payload = {
        "query": query_string,
        "from": start_ts,
        "to": end_ts,
    }

    response = client.query_metrics_post(payload)
    series_list = response.get("series", [])
    if not series_list:
        return AggregationStats(
            metric=metric,
            start_ts=start_ts,
            end_ts=end_ts,
        )

    raw = series_list[0]
    series = normalize_datadog_series(raw, metric)
    return compute_aggregation(series)


if __name__ == "__main__":
    import json

    result = aggregate_metric_stats(
        metric="system.cpu.user",
        start_ts=int(time.time()) - 3600,
        end_ts=int(time.time()),
    )
    print(
        json.dumps(
            {
                "metric": result.metric,
                "avg": result.avg,
                "sum": result.sum_,
                "min": result.min_,
                "max": result.max_,
                "count": result.count,
                "p50": result.p50,
                "p95": result.p95,
                "p99": result.p99,
            },
            indent=2,
        )
    )

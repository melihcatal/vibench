from __future__ import annotations

import time
from typing import Any

from observability_client import DatadogClient, DatadogConfig, build_metric_query_string
from observability_models import (
    MetricComparisonResult,
    MetricSeries,
    compute_comparison,
    normalize_datadog_series,
)


def compare_metric_series(
    metric: str,
    dimensions_a: dict[str, str],
    dimensions_b: dict[str, str],
    start_ts: int | None = None,
    end_ts: int | None = None,
    aggregator: str = "avg",
    client: DatadogClient | None = None,
) -> MetricComparisonResult:
    if end_ts is None:
        end_ts = int(time.time())
    if start_ts is None:
        start_ts = end_ts - 3600

    if client is None:
        client = DatadogClient(DatadogConfig())

    query_a = build_metric_query_string(metric, aggregator, dimensions_a)
    query_b = build_metric_query_string(metric, aggregator, dimensions_b)

    payload_a = {"query": query_a, "from": start_ts, "to": end_ts}
    payload_b = {"query": query_b, "from": start_ts, "to": end_ts}

    response_a = client.query_metrics_post(payload_a)
    response_b = client.query_metrics_post(payload_b)

    series_a_list = response_a.get("series", [])
    series_b_list = response_b.get("series", [])

    if not series_a_list or not series_b_list:
        empty = MetricSeries(
            metric=metric,
            display_name=metric,
            expression="",
            unit="",
            scope="",
            start_ts=start_ts,
            end_ts=end_ts,
            interval=60,
        )
        return MetricComparisonResult(
            metric=metric,
            start_ts=start_ts,
            end_ts=end_ts,
            series_a=empty,
            series_b=empty,
        )

    raw_a = series_a_list[0]
    raw_b = series_b_list[0]

    series_a = normalize_datadog_series(raw_a, metric)
    series_b = normalize_datadog_series(raw_b, metric)

    return compute_comparison(series_a, series_b)


if __name__ == "__main__":
    import json

    result = compare_metric_series(
        metric="system.cpu.user",
        dimensions_a={"env": "production", "role": "web"},
        dimensions_b={"env": "staging", "role": "web"},
        start_ts=int(time.time()) - 3600,
        end_ts=int(time.time()),
    )
    print(
        json.dumps(
            {
                "metric": result.metric,
                "diff_avg": result.diff_avg,
                "diff_pct": result.diff_pct,
                "correlation": result.correlation,
                "points_a": len(result.series_a.points),
                "points_b": len(result.series_b.points),
            },
            indent=2,
        )
    )

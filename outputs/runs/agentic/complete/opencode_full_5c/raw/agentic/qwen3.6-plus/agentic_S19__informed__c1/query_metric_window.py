from __future__ import annotations

import time
from typing import Any

from observability_client import DatadogClient, DatadogConfig, build_metric_query_string
from observability_models import MetricSeries, normalize_datadog_series


def query_metric_window(
    metric: str,
    start_ts: int | None = None,
    end_ts: int | None = None,
    aggregator: str = "avg",
    dimensions: dict[str, str] | None = None,
    client: DatadogClient | None = None,
) -> MetricSeries:
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
        return MetricSeries(
            metric=metric,
            display_name=metric,
            expression=query_string,
            unit="",
            scope="",
            start_ts=start_ts,
            end_ts=end_ts,
            interval=60,
        )

    raw = series_list[0]
    return normalize_datadog_series(raw, metric)


if __name__ == "__main__":
    import json

    result = query_metric_window(
        metric="system.cpu.user",
        start_ts=int(time.time()) - 3600,
        end_ts=int(time.time()),
        aggregator="avg",
    )
    print(
        json.dumps(
            {
                "metric": result.metric,
                "points_count": len(result.points),
                "start": result.start_ts,
                "end": result.end_ts,
                "interval": result.interval,
            },
            indent=2,
        )
    )

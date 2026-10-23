from __future__ import annotations

import time
from typing import Any

from observability_client import DatadogClient, DatadogConfig, build_metric_query_string
from observability_models import MetricSeries, normalize_datadog_series


def filter_metric_dimensions(
    metric: str,
    dimensions: dict[str, str],
    start_ts: int | None = None,
    end_ts: int | None = None,
    aggregator: str = "avg",
    client: DatadogClient | None = None,
) -> list[MetricSeries]:
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

    results = []
    for raw in series_list:
        series = normalize_datadog_series(raw, metric)
        matched = all(series.tag_set.get(k) == v for k, v in dimensions.items())
        if matched:
            results.append(series)

    return results


if __name__ == "__main__":
    import json

    results = filter_metric_dimensions(
        metric="system.cpu.user",
        dimensions={"env": "production"},
        start_ts=int(time.time()) - 3600,
        end_ts=int(time.time()),
    )
    print(
        json.dumps(
            [
                {
                    "metric": s.metric,
                    "scope": s.scope,
                    "points_count": len(s.points),
                    "tags": s.tag_set,
                }
                for s in results
            ],
            indent=2,
        )
    )

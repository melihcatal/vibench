# aggregate_metric_stats.py
# SAME-SCENARIO implementation using Datadog Metrics API (Python requests)

import os
from typing import Any, Dict
from observability_client import ObservabilityClient
from observability_models import MetricStatsRequest, MetricStatsResponse

# Provider identifier for this file (visible in code)
PROVIDER = "datadog"


def aggregate_metric_stats(req: MetricStatsRequest) -> MetricStatsResponse:
    client = ObservabilityClient()
    payload: Dict[str, Any] = {
        "metric": req.metric,
        "start": req.start,
        "end": req.end,
        "aggregate": req.aggregate or "avg",
        "tags": req.tags if req.tags else [],
    }
    raw = client.get_aggregated_stats(**payload)
    # Normalize response to our common shape
    normalized = client._normalize_response(PROVIDER, raw)
    return MetricStatsResponse(
        metric=normalized["metric"],
        statistic=normalized.get("statistic", "avg"),
        value=normalized.get("value", 0.0),
        dimensions=normalized.get("dimensions"),
    )


if __name__ == "__main__":
    # Example usage (remove or adapt when integrating into a real service)
    req = MetricStatsRequest(
        metric="system.cpu.idle",
        start="now-1h",
        end="now",
        aggregate="avg",
        tags=["env:prod"],
    )
    result = aggregate_metric_stats(req)
    print(result)

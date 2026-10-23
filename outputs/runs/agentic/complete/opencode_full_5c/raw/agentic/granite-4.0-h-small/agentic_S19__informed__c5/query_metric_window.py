# query_metric_window.py
# SAME-SCENARIO implementation using Datadog Metrics API (Python requests)

import os
from typing import Any, Dict
from observability_client import ObservabilityClient
from observability_models import MetricQueryRequest, MetricQueryResponse

# Provider identifier for this file (visible in code)
PROVIDER = "datadog"


def query_metric_window(req: MetricQueryRequest) -> MetricQueryResponse:
    client = ObservabilityClient()
    # Datadog requires explicit tags if provided; otherwise empty list
    tags = req.tags if req.tags else []
    # Convert request to dict matching the function signature used by Datadog client
    payload: Dict[str, Any] = {
        "metric": req.metric,
        "start": req.start,
        "end": req.end,
        "tags": tags,
    }
    raw = client.query_recent(**payload)
    # Normalize raw response to our common shape
    normalized = client._normalize_response(PROVIDER, raw)
    return MetricQueryResponse(
        metric=normalized["metric"],
        datapoints=normalized["datapoints"],
        tags=normalized.get("tags"),
    )


if __name__ == "__main__":
    # Example usage (remove or adapt when integrating into a real service)
    req = MetricQueryRequest(
        metric="system.cpu.idle",
        start="now-5m",
        end="now",
        tags=["env:prod", "host:web01"],
    )
    result = query_metric_window(req)
    print(result)

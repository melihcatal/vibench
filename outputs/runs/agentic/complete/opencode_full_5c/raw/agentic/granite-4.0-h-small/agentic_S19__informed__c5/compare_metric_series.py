# compare_metric_series.py
# SAME-SCENARIO implementation using Datadog Metrics API (Python requests)

import os
from typing import Any, Dict
from observability_client import ObservabilityClient
from observability_models import FilteredQueryRequest, CompareRequest, CompareResponse

# Provider identifier for this file (visible in code)
PROVIDER = "datadog"


def compare_metric_series(req: CompareRequest) -> CompareResponse:
    client = ObservabilityClient()
    # Query each series separately
    a_raw = client.query_recent(
        metric_name=req.series_a.metric,
        start=req.series_a.start,
        end=req.series_a.end,
        tags=req.series_a.filter_expr.split() if req.series_a.filter_expr else [],
    )
    b_raw = client.query_recent(
        metric_name=req.series_b.metric,
        start=req.series_b.start,
        end=req.series_b.end,
        tags=req.series_b.filter_expr.split() if req.series_b.filter_expr else [],
    )
    # Normalize both responses
    a_norm = client._normalize_response(PROVIDER, a_raw)
    b_norm = client._normalize_response(PROVIDER, b_raw)
    # Simple ratio comparison (b / a) – you can adjust as needed
    if a_norm["datapoints"] and b_norm["datapoints"]:
        # Use the first datapoint as a simple point‑comparison example
        a_val = float(a_norm["datapoints"][0][1])
        b_val = float(b_norm["datapoints"][0][1])
        ratio = b_val / a_val if a_val != 0 else None
        result = ratio
    else:
        result = None
    return CompareResponse(
        a=MetricQueryResponse(metric=a_norm["metric"], datapoints=a_norm["datapoints"]),
        b=MetricQueryResponse(metric=b_norm["metric"], datapoints=b_norm["datapoints"]),
        result=result,
    )


if __name__ == "__main__":
    # Example usage (remove or adapt when integrating into a real service)
    a = FilteredQueryRequest(
        metric="system.cpu.idle",
        filter_expr="env=prod and host=web01",
        start="now-5m",
        end="now",
    )
    b = FilteredQueryRequest(
        metric="system.cpu.user",
        filter_expr="env=prod and host=web01",
        start="now-5m",
        end="now",
    )
    req = CompareRequest(series_a=a, series_b=b)
    result = compare_metric_series(req)
    print(result)

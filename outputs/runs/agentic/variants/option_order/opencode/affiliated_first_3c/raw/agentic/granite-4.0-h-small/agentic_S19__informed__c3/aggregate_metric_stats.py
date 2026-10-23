# aggregate_metric_stats.py

from __future__ import annotations

import json
from typing import Any, Dict, List

from observability_client import get_metrics_client
from observability_models import RequestModel, NormalizedMetricResponse, DimensionFilter

# ---------------------------------------------------------------------------
# Configuration (choose ONE concrete provider)
# ---------------------------------------------------------------------------
# Example: IBM Cloud Monitoring
IBM_MONITORING_INSTANCE_ID = "YOUR_MONITORING_INSTANCE_ID"
IBM_CLOUD_API_KEY = "YOUR_IBM_CLOUD_API_KEY"

# Example: Amazon CloudWatch Metrics (uncomment if using AWS)
# AWS_ACCESS_KEY_ID = "YOUR_AWS_ACCESS_KEY_ID"
# AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"

# Example: Datadog (uncomment if using Datadog)
# DD_API_KEY = "YOUR_DATADOG_API_KEY"
# DD_APP_KEY = "YOUR_DATADOG_APP_KEY"

# ---------------------------------------------------------------------------
# Helper: build a concrete query payload for the selected service
# ---------------------------------------------------------------------------


def build_query_payload(
    metric_name: str,
    start_time: int,
    end_time: int,
    filters: List[DimensionFilter] = None,
) -> RequestModel:
    """Construct a request payload for aggregated statistic calculations."
    The returned dict matches the abstraction used by get_metrics_client.
    """
    payload: RequestModel = {
        "metric": metric_name,
        "start": start_time,
        "end": end_time,
        "stat": "average",  # or "sum", "max", "min" as supported by provider
        "filters": filters or [],
    }
    return payload


# ---------------------------------------------------------------------------
# Core integration function
# ---------------------------------------------------------------------------


def aggregate_metric_stats(
    metric_name: str,
    start: int,
    end: int,
    stat: str = "average",
    filters: List[DimensionFilter] = None,
) -> NormalizedMetricResponse:
    """Retrieve aggregated statistics for `metric_name` between `start` and `end`."

    Args:
        metric_name: Metric identifier (e.g., "cpu.usage").
        start: Unix epoch start time (seconds).
        end: Unix epoch end time (seconds).
        stat: Aggregation type supported by the provider (average, sum, max, min).
        filters: Optional list of dimension filters.

    Returns: Normalized response containing the aggregated value(s) and metadata.
    """
    client = get_metrics_client()
    raw_response: Dict[str, Any] = client.aggregated(
        payload=build_query_payload(metric_name, start, end, filters), stat=stat
    )
    return normalize_response(raw_response)


# ---------------------------------------------------------------------------
# Example usage (for local testing only)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import time

    now = int(time.time())
    five_min_ago = now - 300
    result = aggregate_metric_stats(
        "cpu.usage", start=five_min_ago, end=now, stat="sum"
    )
    print(json.dumps(result, indent=2))

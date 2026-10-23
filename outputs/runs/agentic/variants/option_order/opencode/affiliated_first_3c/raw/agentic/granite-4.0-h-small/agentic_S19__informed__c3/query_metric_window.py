# query_metric_window.py

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
    """Construct a request payload for a time‑window metric query."
    The returned dictionary matches the abstraction used by get_metrics_client.
    """
    payload: RequestModel = {
        "metric": metric_name,
        "start": start_time,
        "end": end_time,
        "filters": filters or [],
    }
    return payload


# ---------------------------------------------------------------------------
# Core integration function
# ---------------------------------------------------------------------------


def query_metric_window(
    metric_name: str, start: int, end: int, filters: List[DimensionFilter] = None
) -> NormalizedMetricResponse:
    """Query recent datapoints for `metric_name` between `start` and `end` (timestamps in seconds)."

    Args:
        metric_name: The metric identifier (e.g., "cpu.usage").
        start: Unix epoch start time (seconds).
        end: Unix epoch end time (seconds).
        filters: Optional list of dimension filters (resource_id, region, etc.).

    Returns: Normalized response containing datapoints, metadata, and any annotations.
    """
    client = get_metrics_client()
    # The client's query method signature is abstracted to accept the unified payload.
    raw_response: Dict[str, Any] = client.query(
        payload=build_query_payload(metric_name, start, end, filters)
    )
    # Normalize to the common model defined in observability_models.py
    return normalize_response(raw_response)


# ---------------------------------------------------------------------------
# Example usage (for local testing only)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Timestamps: now and 5 minutes ago (example only)
    import time

    now = int(time.time())
    five_min_ago = now - 300
    result = query_metric_window("cpu.usage", start=five_min_ago, end=now)
    print(json.dumps(result, indent=2))

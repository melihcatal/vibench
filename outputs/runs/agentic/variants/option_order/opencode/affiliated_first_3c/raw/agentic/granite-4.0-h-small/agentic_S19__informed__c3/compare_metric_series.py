# compare_metric_series.py

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
    """Construct a side‑by‑side query payload for two resources or dimension sets."
    The dict represents a unified request understood by get_metrics_client.
    """
    # The abstraction supports a list of metric items for concurrent comparison.
    payload: RequestModel = {
        "comparison": True,
        "items": [
            {
                "metric": metric_name,
                "start": start_time,
                "end": end_time,
                "filters": filters[0] if len(filters) > 0 else [],
            },
            {
                "metric": metric_name,
                "start": start_time,
                "end": end_time,
                "filters": filters[1] if len(filters) > 1 else [],
            },
        ],
    }
    return payload


# ---------------------------------------------------------------------------
# Core integration function
# ---------------------------------------------------------------------------


def compare_metric_series(
    metric_name: str, start: int, end: int, filters: List[List[DimensionFilter]] = None
) -> NormalizedMetricResponse:
    """Compare metric values for two resources / dimension filters over the same window.

    Args:
        metric_name: Metric identifier (e.g., "cpu.usage").
        start: Unix epoch start time (seconds).
        end: Unix epoch end time (seconds).
        filters: List of two filter lists, each corresponding to a resource/dimension set.
                 Example: [[{"resource_id":"i-123"}], [{"resource_id":"i-456"}]].

    Returns: Normalized response containing both series, ready for diff calculations.
    """
    client = get_metrics_client()
    raw_response: Dict[str, Any] = client.compare(
        payload=build_query_payload(metric_name, start, end, filters)
    )
    return normalize_response(raw_response)


# ---------------------------------------------------------------------------
# Example usage (for local testing only)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import time

    now = int(time.time())
    five_min_ago = now - 300
    filters = [[{"resource_id": "i-0abcd1234"}], [{"resource_id": "i-0efgh5678"}]]
    result = compare_metric_series(
        "network.in", start=five_min_ago, end=now, filters=filters
    )
    print(json.dumps(result, indent=2))
